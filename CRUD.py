import datetime

users = {}
folders = {}
labels = {}
files = {}

folder_id = 1000
label_id = 0
file_id = 0

commandAction = {}


def Init():
    commandAction["register"] = register
    commandAction["create_folder"] = create_folder
    commandAction["delete_folder"] = delete_folder
    commandAction["get_folders"] = get_folders
    commandAction["rename_folder"] = rename_folder
    commandAction["upload_file"] = upload_file
    commandAction["delete_file"] = delete_file
    commandAction["get_files"] = get_files
    commandAction["add_label"] = add_label
    commandAction["get_labels"] = get_labels
    commandAction["delete_label"] = delete_label
    commandAction["add_folder_label"] = add_folder_label
    commandAction["delete_folder_label"] = delete_folder_label


def action(_action, totalCommand):
    if _action not in commandAction:
        print("Unknown action: " + _action)
        return
    # print("do action : " + str(_action))
    ans = commandAction[_action](totalCommand)
    print(ans)


def register(input_str_list):

    if len(input_str_list) != 2:
        return "Invalid input format. Usage: register <username>"

    username = input_str_list[1]
    if compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - user already existing")

    users[username] = {}
    return ('Success')


def create_folder(input_str_list):

    inputStrLen = len(input_str_list)
    if inputStrLen != 4 and inputStrLen != 3:
        return "Invalid input format. Usage: create_folder {username} {folder_name} {description}"
    username = input_str_list[1]
    folder_name = input_str_list[2]
    if inputStrLen == 3:
        description = ""
    else:
        description = input_str_list[3]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return "Error - unknown user"

    if compareStrIsInDicWithCaseInsensitive(folder_name, folders, "name"):
        return "Error - folder name already existing"

    global folder_id

    folder_id += 1
    strId = str(folder_id)
    folders[strId] = {"id": strId, "label": "", "name": folder_name, "description": description,
                      "created_at": str(datetime.datetime.now()), "owner": username, "files": {}}

    return strId


def delete_folder(input_str_list):

    if len(input_str_list) != 3:
        return "Invalid input format. Usage: delete_folder {username} {folder_id}"

    username = input_str_list[1]
    folder_id = input_str_list[2]

    if folder_id not in folders:
        return "Error - folder doesn't exist"

    if folders[folder_id]["owner"].lower() != username.lower():
        return "Error - folder owner not match"

    del folders[folder_id]
    return "Success"


def get_folders(input_str_list):
    inputLen = len(input_str_list)
    if inputLen != 4 and inputLen != 5:
        return "Invalid input format. Usage: get_folders {username} {sort_name | sort_time} {asc|dsc} or get_folders {username} {label_name} {sort_name | sort_time} {asc|dsc} "

    username = input_str_list[1]
    if inputLen == 4:
        sort = input_str_list[2]
        order = input_str_list[3]
    else:
        label_name = input_str_list[2]
        sort = input_str_list[3]
        order = input_str_list[4]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return "Error - unknown users"

    if sort not in ["sort_name", "sort_time"]:
        return "Error - invalid sort type"
    if order not in ["asc", "dsc"]:
        return "Error - invalid sort order"

    if inputLen == 5:
        if not compareStrIsInDicWithCaseInsensitive(label_name, labels):
            return "Error - the label is not exists"
    #
    folder_list = []
    folder_list_byUser = []
    for _, folder_data in folders.items():
        if folder_data["owner"] == username:
            folder_list_byUser.append((folder_data["name"], folder_data))

    if inputLen == 4:
        folder_list = folder_list_byUser
    else:
        folder_list_byLabel = []
        for folder_data in folder_list_byUser:
            if folder_data[1] == label_name:
                folder_list_byLabel.append((folder_data["name"], folder_data))
        folder_list = folder_list_byLabel
    #
    if sort == "sort_name":
        folder_list = sorted(folder_list, key=lambda x: x[0])
    else:
        folder_list = sorted(folder_list, key=lambda x: x[1]["created_at"])

    if order == "dsc":
        folder_list = reversed(folder_list)

    output = []
    for folder_name, folder_data in folder_list:
        print("id :" + str(folder_data['id']) + ", name :" + folder_name)
        output.append(
            str(folder_data['id']) + "|" + folder_name + "|" + str(folder_data['description']) + "|" + str(folder_data['created_at']) + "|" + str(folder_data['owner']))

    if len(output) == 0:
        return "Warning - empty folders"

    return "\n".join(output)


def rename_folder(input_str_list):

    if len(input_str_list) != 4:
        return "Invalid input format. Usage: rename_folders {username} {folder_id} {new_folder_name}"

    username = input_str_list[1]
    folder_id = input_str_list[2]
    new_folder_name = input_str_list[3]

    if folder_id not in folders:
        return "Error - folder_id not found"

    if folders[folder_id]["owner"].lower() != username.lower():
        return "Error - unknown user"

    folders[folder_id]["name"] = new_folder_name
    return "Success"


def upload_file(input_str_list):

    inputStrLen = len(input_str_list)
    if inputStrLen != 5 and inputStrLen != 4:
        return "Invalid input format. Usage: upload_file {username} {folder_id} {file_name} {description}"

    username = input_str_list[1]
    folder_id = input_str_list[2]
    file_name = input_str_list[3]
    if inputStrLen == 4:
        description = ""
    else:
        description = input_str_list[4]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return "Error - unknown user"

    if folder_id not in folders:
        return "Error - folder_id not found"

    file_name_split = file_name.split(".")
    if len(file_name_split) < 2:
        return "Error - file format is wrong"
    extension = ".".join(file_name_split[1:])

    if compareStrIsInDicWithCaseSsensitive(file_name, files, "name"):
        return "Error - file name already existing"

    global file_id
    file_id += 1
    folders[folder_id]["files"][file_name] = {"id": str(file_id), "name": file_name, "extension": extension, "description": description,
                                              "created_at": str(datetime.datetime.now()), "owner": username}
    files[file_name] = {"id": str(file_id), "name": file_name, "extension": extension, "description": description,
                        "created_at": str(datetime.datetime.now()), "owner": username}

    return "Success"


def delete_file(input_str_list):

    if len(input_str_list) != 4:
        return "Invalid input format. Usage: delete_file {username} {folder_id} {file_name}"

    username = input_str_list[1]
    folder_id = input_str_list[2]
    file_name = input_str_list[3]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return "Error - unknown user"

    if folder_id not in folders:
        return "Error - folder_id not found"

    if file_name not in folders[folder_id]["files"]:
        return "Error - file_name not found"

    if folders[folder_id]["owner"].lower() != username.lower():
        print("Warning  - folder owner not match")

    del folders[folder_id]["files"][file_name]
    return "Success"


def get_files(input_str_list):

    if len(input_str_list) != 5:
        return "Invalid input format. Usage: get_files {username} {folder_id} {sort_name|sort_time|sort_extension} {asc|dsc}"

    username = input_str_list[1]
    folder_id = input_str_list[2]
    sort_type = input_str_list[3]
    sort_order = input_str_list[4]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return "Error - unknown user"

    if folder_id not in folders:
        return "Error - folder_id not found"

    if sort_type not in ["sort_name", "sort_time", "sort_extension"]:
        return "Error - invalid sort type"

    if sort_order not in ["asc", "dsc"]:
        return "Error - invalid sort order"

    _files = []

    for file_id in folders[folder_id]["files"]:
        _files.append(files[file_id])

    if len(_files) == 0:
        return "Warning - empty files"

    if sort_type == "sort_name":
        sorted_files = sorted(_files, key=lambda file: file["name"])
    elif sort_type == "sort_time":
        sorted_files = sorted(_files, key=lambda file: file["created_at"])
    else:
        sorted_files = sorted(_files, key=lambda file: file["extension"])

    if sort_order == "dsc":
        sorted_files = reversed(sorted_files)

    results = []
    for file_data in sorted_files:
        result_str = file_data["name"] + "|" + file_data["extension"] + "|" + \
            file_data["description"] + "|" + \
            file_data["created_at"] + "|" + file_data["owner"]
        results.append(result_str)

    return "\n".join(results)


def add_label(input_str_list):

    if len(input_str_list) != 4:
        return ("Invalid input format. Usage: add_label {username} {label_name} {color}")
    username = input_str_list[1]
    label_name = input_str_list[2]
    color = input_str_list[3]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - unknown user")

    if compareStrIsInDicWithCaseInsensitive(label_name, labels):
        return ("Error - the label name existing")

    global label_id

    label_id += 1
    strId = str(label_id)
    labels[label_name] = {"id": strId, "name": label_name, "color": color,
                          "created_at": str(datetime.datetime.now()), "owner": username}

    return "Success"


def get_labels(input_str_list):
    if len(input_str_list) != 2:
        return ("Invalid input format. Usage: get_labels {username}")
    username = input_str_list[1]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - unknown user")

    _labels = []
    for _, lableData in labels.items():
        if lableData["owner"].lower() == username.lower():
            _labels.append(lableData)

    output = []
    for label in _labels:
        output.append(label["name"] + "|" + str(label["color"]) +
                      "|" + label["created_at"] + "|" + label["owner"])

    if len(output) == 0:
        return ("Error - the user have no label")

    return "\n".join(output)


def delete_label(input_str_list):
    if len(input_str_list) != 3:
        return ("Invalid input format. Usage: delete_labels {username} {label_name}")
    username = input_str_list[1]
    label_name = input_str_list[2]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - unknown user")

    if not compareStrIsInDicWithCaseInsensitive(label_name, labels):
        return ("Error - the label name not exist")

    if labels[label_name]["owner"].lower() != username.lower():
        return ("Error - owner mismatch")

    del (labels[label_name])
    return "Success"


def add_folder_label(input_str_list):
    if len(input_str_list) != 4:
        return ("Invalid input format. Usage: add_folder_label {username} {folder_id} {label_name}")
    username = input_str_list[1]
    folder_id = input_str_list[2]
    label_name = input_str_list[3]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - unknown user")

    if not compareStrIsInDicWithCaseInsensitive(label_name, labels):
        return ("Error - the label name not exist")

    if folder_id not in folders:
        return ("Error - folder not exist")

    folders[folder_id]["label"] = label_name
    return "Success"


def delete_folder_label(input_str_list):
    if len(input_str_list) != 4:
        return ("Invalid input format. Usage: delete_folder_label {username} {folder_id} {label_name}")
    username = input_str_list[1]
    folder_id = input_str_list[2]
    label_name = input_str_list[3]

    if not compareStrIsInDicWithCaseInsensitive(username, users):
        return ("Error - unknown user")

    if folder_id not in folders:
        return ("Error - folder not exist")

    folders[folder_id]["label"] = ""
    return "Success"


def compareStrIsInDicWithCaseInsensitive(inputStr, dict, value=""):
    if value == "":
        if inputStr.lower() in map(str.lower, dict.keys()):
            return True
        else:
            return False
    else:
        for dictData in dict.values():
            if dictData[value].lower() == inputStr.lower():
                return True
        return False


def compareStrIsInDicWithCaseSsensitive(inputStr, dict, value=""):
    if value == "":
        if inputStr in dict:
            return True
        else:
            return False
    else:
        for dictData in dict.values():
            if dictData[value] == inputStr:
                return True
        return False
