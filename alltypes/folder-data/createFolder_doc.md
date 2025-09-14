# Documentation Title: Create Folder

## Create a folder in CTMS

#### Summary:
The Interplay Web Services method CreateFolder creates a folder or nested path of folders. The method CreateFolders creates multiple folders or nested paths of folders. Optionally, the owner of the folder can be set.

> In CTMS you can create only one direct sub folder to an existing folder with a single call. To create a path of folders, you must create them subfolder by subfolder. To create multiple folders, you must also create them one by one.

###### Parameter:
- The ID of an existing folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".
- The name of the sub folder to create.

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an   URI template.
    1. Set the URI template variable "id" to the ID of the folder and expand the URI template.
    2. Make an HTTP GET request to get the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the folder.
3. Call HTTP POST on the [loc:create-folder](https://developer.avid.com/ctms/api/loc/linkrels/create-folder.html) link with a JSON message body like this:

    ```
    {
    "common": {
        "name": "Name of new folder"
        }
    }
    ```

> In CTMS, the caller of [loc:create-folder](https://developer.avid.com/ctms/api/loc/linkrels/create-folder.html) is set as owner of the new folder.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Create Folder/CTMS Create Folder User Input.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **folder ID** in the environment variable named: folderIdInput</mark>

> **GET** 2_loc item by id
- Hitting the above fetched selected_system_locItemByIdHref, to get the folder information for the given folder ID.
- In the **Scripts** section: We fetch "[loc:create-folder](https://developer.avid.com/ctms/api/loc/linkrels/create-folder.html)" link to fetch the link for creating a new folder in the desired location, and store it globally as selected_system_createSubFolder.
    
> **POST** 3_create Folder Inside Desired Location
- Hitting the above selected_system_createSubFolder, to create a sub folder inside the given path.
- In the **Body** section: we provide the "common" value with the name of the new sub folder that we want to create.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.