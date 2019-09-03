import sys
import os
import argparse
import json
import shutil


INVALID_PLAYLIST_DATA_STR = """FAILED TO RUN: The change data is not coherent. For example you are removing a playlist 
while also trying to add a song to that same playlist, or referencing a playlist that does not exist, etc."""

INVALID_SONG_DATA_STR = """FAILED TO RUN: The change data is not coherent. You are adding a song to a new or existing 
playlist, and that song does not exist."""

INVALID_USER_DATA_STR = """FAILED TO RUN: The change data is not coherent. You are referencing a user in the change 
file that does not exist."""

INVALID_SOURCE_FILE_DATA_STR = """UNEXPECTED: The input mixtape.json file is empty."""

INVALID_CHANGES_FILE_DATA_STR = """UNEXPECTED: The input changes-file is empty."""


class PlaylistValidationError(Exception):
   """Raised when the playlist-remove and playlist-add-song changes are not coherent,
   or when a non-existent playlist is referenced."""
   pass

class SongValidationError(Exception):
   """Raised when the playlist-add-song or user-add-playlist changes reference a non-existent song."""
   pass

class UserValidationError(Exception):
   """Raised when the user-add-playlist changes reference a non-existent song."""
   pass

class EmptySourceValidationError(Exception):
   """Raised when the input mixtape.json file is empty."""
   pass

class EmptyChangesValidationError(Exception):
   """Raised when the input changes-file is empty."""
   pass


def getArgs():

    parser = argparse.ArgumentParser(description="Highspot Music App")

    parser.add_argument("input",
                        help="This file contains the original music data")
    parser.add_argument("changes",
                        help="This file contains the metadata representing changes to the original music data")
    parser.add_argument("output",
                        help="This file contains the output after applying the changes to the original music data")

    args = parser.parse_args()

    return args.input, args.changes, args.output


def setup_working_lists_from_changes_file(changes):

    playlists_for_add_song = []     # List of playlists that need to have a song added.
    change_list_songs = []          # List of songs referenced in the change file.
    change_list_users = []          # List of users referenced in the change file.

    if changes.get("playlist_add_song") is not None:
        for obj in changes["playlist_add_song"]:
            playlists_for_add_song.append(obj["playlist_id"])
            change_list_songs.append(obj["song_id"])

    if changes.get("user_add_playlist") is not None:
        for obj in changes["user_add_playlist"]:
            change_list_users.append(obj["user_id"])
            change_list_songs.extend(obj["song_ids"])

    return playlists_for_add_song, changes["playlist_remove"], change_list_songs, change_list_users


def getCurrentList(input, key):

    new_list = []

    if input.get(key) is not None:
        for obj in input[key]:
            new_list.append(obj["id"])

    return new_list


def setup_working_lists_from_original_file(original):

    valid_playlists = []    # List valid playlists.
    valid_songs = []        # List valid songs.
    valid_users = []        # List valid users.

    if original.get("playlists") is not None:
        valid_playlists = getCurrentList(original, "playlists")

    if original.get("songs") is not None:
        valid_songs = getCurrentList(original, "songs")

    if original.get("users") is not None:
        valid_users = getCurrentList(original, "users")

    return valid_playlists, valid_songs, valid_users


def validate_change_data(changes, original):

    # Setup lists used for validation. Some of these are used to do work later.

    playlists_for_add_song, playlists_to_be_removed, change_list_songs, change_list_users \
        = setup_working_lists_from_changes_file(changes)

    valid_playlists, valid_songs, valid_users = setup_working_lists_from_original_file(original)

    # Check that playlists for removal and update do exist.

    for entry in playlists_for_add_song:
        if entry not in valid_playlists:
            raise PlaylistValidationError

    for entry in playlists_to_be_removed:
        if entry not in valid_playlists:
            raise PlaylistValidationError

    # Check that we are not both removing and updating the same playlist.

    for entry in playlists_for_add_song:
        if entry in playlists_to_be_removed:
            raise PlaylistValidationError

    # Check that songs being added to a playlist, or, that are part of a new playlist, exist.

    for entry in change_list_songs:
        if entry not in valid_songs:
            raise SongValidationError

    # Check that users referenced in the changes file exist.

    for entry in change_list_users:
        if entry not in valid_users:
            raise UserValidationError

    return playlists_for_add_song, playlists_to_be_removed, valid_playlists


def playlistUpdates(playlists_for_add_song, playlists_to_be_removed, changes, original):

    # We are creating a new updated playlist.

    updated_playlists =[]

    # Walk through the existing playlists and do the remove and update work.
    # We make one pass through which is efficient - the original file could be quite large (many entries),
    # while we expect the changes file to be much smaller (few entries).

    for pl in original["playlists"]:

        # If a playlist is being removed, we do not add it to the updated list.

        if pl["id"] in playlists_to_be_removed:
            continue

        # The playlist still exists - if we need to add any songs to it, do that now.

        # Add-song could be add-songs (pl.) with a change to the JSON (array rather than single value).
        # The way it is now, you could add 2 songs to 1 playlist, by creating an entry for each song in the
        # changes file.
        # The instructions said 'Add an existing song to an existing playlist.' - implies singular, for production code,
        # I would double check, but this is an exercise.

        if pl["id"] in playlists_for_add_song:

            # Find the matching entry in the changes file.
            # Worst case runtime approaches n^2, where n is the number of playlists, if we are changing every playlist.
            # As above, the assumption is that the changes file is usually a fraction of the size of the original file,
            # which means runtime is more like constant * n.
            # If we knew the real world data would approach n^2, we would explore a log base 2 alternative.

            for entry in changes["playlist_add_song"]:
                if pl["id"] == entry["playlist_id"]:
                    pl["song_ids"].append(entry["song_id"])

            # Sort the original file's song list.

            pl["song_ids"].sort()

        # Add this playlist to our updated list.

        updated_playlists.append(pl)

    # We have completed updates to the list of playlists, set the original file's entry to the updated playlist list.

    original["playlists"] = updated_playlists

    return original


def userAddPlaylist(changes, original):

    # If there is no work to do, return.

    if changes.get("user_add_playlist") is None:
        return original

    for entry in changes["user_add_playlist"]:

        # Find the highest value for a playlist id and increment to get the next value.

        # Note that there is an upper bound, and we are not checking it here. For production code,
        # we would need a check for wrapping.
        # We also ignore 'holes' due to removals.

        highest = 1

        if original.get("playlists") is not None:
            valid_playlists = getCurrentList(original, "playlists")
            valid_playlists.sort(reverse=True)

            highest = int(valid_playlists[0]) + 1

        entry_to_add = entry
        entry_to_add["id"] = str(highest)

        original["playlists"].append(entry_to_add)

    return original


def main():

    try:

        # Print the Python version being used.

        print('Using Python version: ', sys.version[:5], '\n')

        # Get the 3 file names from the command line args.

        original_file, changes_file, output_file  = getArgs()

        # If either the original or changes files are empty, just copy original to the output file,
        # but this needs clarification, see below.

        if not os.path.getsize(original_file):
            shutil.copyfile(original_file, output_file)
            raise EmptySourceValidationError

        if not os.path.getsize(changes_file):
            shutil.copyfile(original_file, output_file)
            raise EmptyChangesValidationError

        # Open the original and changes files and load to local vars.

        with open(original_file) as fo:
            original = json.load(fo)

        with open(changes_file) as fo:
            changes = json.load(fo)

        # Check that the change file does not have any obvious errors before going any farther.

        playlists_for_add_song, playlists_to_be_removed, valid_playlists = validate_change_data(changes, original)

        # Do the playlist updates - remove playlist, add song to playlist.

        original = playlistUpdates(playlists_for_add_song, playlists_to_be_removed, changes, original)

        # Now add the new playlists.

        original = userAddPlaylist(changes, original)

        # Open the output file, dump the resulting JSON to this file.

        with open(output_file, "w") as fo:
            json.dump(original, fo, sort_keys=True, indent=4)

    except PlaylistValidationError:
        print(INVALID_PLAYLIST_DATA_STR)
        exit(1)

    except SongValidationError:
        print(INVALID_SONG_DATA_STR)
        exit(1)

    except UserValidationError:
        print(INVALID_USER_DATA_STR)
        exit(1)

    # What to do with empty files needs clarification - silently succeed or flag as unexpected?
    # Doing the latter here, but would need clarification for production code.

    except EmptySourceValidationError:
        print(INVALID_SOURCE_FILE_DATA_STR)
        exit(1)

    # If called with an empty changes-file, we return success, no changes to apply. Same as above, needs clarification.

    except EmptyChangesValidationError:
        print(INVALID_CHANGES_FILE_DATA_STR)

if __name__ == '__main__':
    main()