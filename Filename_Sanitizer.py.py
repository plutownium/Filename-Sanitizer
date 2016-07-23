import os
import sys
import itertools
import time
from time import sleep
# I'll rewrite it with classes later.

print ("Welcome to Roland's file renaming script. "
       "\nDISCLAIMER: It's recommended that you first "
       "BACK UP THE FOLDER before running this program.\n")
print ("Instructions: Drop this file inside a folder with poorly named .mp3 "
       "files. Follow along with the questions.\n**** CLOSE ALL MUSIC PROGRAMS & PLAYERS BEFORE RUNNING THIS! ****\n")
firstcheck = raw_input("Proceed? [Y] [N] (To undo changes, type 'UNDO'.)\n>"
                       ).upper()

if firstcheck == "Y":
    print ("Say farewell to junk in your file names!")
    if not os.path.isfile("changelog.txt"):
        #  Should create "changelog.txt" if one doesn't exist yet.
        f = open("changelog.txt", "w")
        f.write("###                                  ###\n"
                "### DO NOT EDIT OR DELETE THIS FILE. ###\n"
                "### IT ALLOWS YOU TO UNDO MISTAKES!! ###\n"
                "###                                  ###\n")
        f.close()
    else:
        pass
elif firstcheck == "UNDO":
    if not os.path.isfile("changelog.txt"):
        print "Restart the program, you've got nothing to change!"
        sleep(1)
        sys.exit()
    else:
        pass
    # Opens changelog.txt and attempts to undo most recent changes.
    undo_file = open("changelog.txt", "r")
    change_text = undo_file.read()
    undo_file.close()
    # Stores the index of the most recent change's date/time info.
    last_change_index = change_text.rfind("Your changes were made on: "
                                    ) + len("Your changes were made on: ")
    # Stores the most recent change's date/time info as a string.
    last_change_time = change_text[last_change_index:(last_change_index + 17)]
    revert_data = change_text[(last_change_index + 17):-1]  # That -2 is key.
    revert_data = revert_data.split("\n<< Changed >> ")
    del revert_data[0]  # Delete the empty string at index 0
    title_pairs = [text.split("\n<< To..... >> ") for text in revert_data]
    # This for loop goes through the folder and renames files to their unedited names.
    for names in title_pairs:
        broken_name = item[1]
        filename_original = item[0]
        print filename_original
        print broken_name
        os.rename(broken_name, filename_original)
    sleep(2)
    sys.exit()
else:
    print "Go back up your files and come back."
    sleep(1)
    sys.exit()


def file_list_generator():  # add filepath as an argument later?
    """Returns a list of the files in the current directory."""
    files_list = os.listdir(os.getcwd())
    for item in files_list:
        ismp3 = item[-2:]
        if ismp3 != "p3":
            files_list.remove(item)
    print "Here's all the .mp3 files in the directory: "
    sleep(1.2)
    for item in files_list:
        print item
    return files_list


def file_name_splitter(list_to_split):
    """Splits the names in files_list into another list for later use"""
    file_names_split = []
    for item in list_to_split:
        file_names_split.append(item.split(" "))
    return file_names_split


def word_counter(input_list):
    """returns a dictionary of how many times each item in the list occurs"""
    all_items = []
    avoid_items = ["-", ".mp3", "(Original", "Mix)", "Mix).mp3", "Original",
                   "feat", "feat.", "ft", "Ft", "(feat"]

    for item in input_list:
        for entry in item:
            all_items.append(entry)
    for discard in all_items:
        if discard in avoid_items:
            all_items.remove(discard)
    sorted_items = [list(g) for k, g in itertools.groupby(sorted(all_items))]
    # for item in sorted_items: (disabled)
    #    print len(item), item
    return sorted_items


def sanitizer_input():  # LATER: Add an argument; "user_prompt"?
    """Prompts the user to pick a phrase to delete from the files' names."""
    response = raw_input(
        "Select a phrase to be deleted from file names? "
        "Only items separated by a space will work. [Y] [N]\n>").upper()

    if response == "Y":
        for item in sorted_items:
            print "Entry number: " + str(
                int(sorted_items.index(item) + 1)) + ", " + "Occurs " + str(
                            len(item)) + " times." + str(item)
        selection = raw_input("Which one? Enter the entry number.\n>")
        selection = int(selection) - 1
        sanitizer_target = sorted_items[selection]
        confirmation = \
            raw_input("<<CONFIRMATION>> Delete %s?\n"
                      "[Y] = Confirm, [N] = Repick selection. "
                      "Closing the program here will leave your files unedited.\n>"
                      % sanitizer_target).upper()
        if confirmation == "Y":
            return sanitizer_target
        else:  # will this else statement loop back into the function...?
            sanitizer_input()
    else:
        exit_choice = raw_input("Want to exit the program? [Y] [N]\n>").upper()
        if exit_choice == "Y":
            print "Goodbye."
            sleep(1)
            sys.exit()
        else:
            print "Let's try this again then."
            sanitizer_input()


def filename_sanitizer(original_fileslist, input_target):
    """This loops over the entries in the original list of file names and
    removes every instance of 'sanitizer_target' via .split(). The string
    is then concatenated back together and used to rename the file."""
    target = input_target[0]
    changelog_temp = []
    for item in original_fileslist:
        split_list = item.split(" " + target)
        if len(split_list) > 1:
            newname = split_list[0] + split_list[1]
            if not newname.endswith(".mp3"):
                newname = newname + ".mp3"
            os.rename(item, newname)
            changelog_temp.append([item, newname])
            print "New file name: " + newname
    changelog_updater(changelog_temp)
    print "Done! Go check out your new filenames."


def changelog_updater(changes_to_add_list):
    current_date = "Your changes were made on: %s\n" \
                   % str(time.strftime("%c"))
    changelog_file = open("changelog.txt", "a")
    changelog_file.write(current_date)
    for item in changes_to_add_list:
        origname = item[0]
        newname = item[1]
        added_changes = "<< Changed >> " + str(origname) + "\n" +\
                        "<< To..... >> " + str(newname) + "\n"
        changelog_file.write(added_changes)
    changelog_file.close()





orig_list_of_files = file_list_generator()
file_names_split = file_name_splitter(orig_list_of_files)
sorted_items = word_counter(file_names_split)
sanitizer_target = sanitizer_input()
filename_sanitizer(orig_list_of_files, sanitizer_target)


sys.exit()
