# Documentation Title: Add Asset to Folder (LinkToMob)

#### Summary:
The Interplay Web Services method LinkToMOB adds a reference to an asset, identified by its MOB ID, to a folder. 

## Add an asset to a folder in CTMS

###### Parameters:
- The MOB ID of the asset.
- The ID of the target folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    1. Set the URI template variable "id" to the ID of the target folder and expand the URI template.
    2. Make an HTTP GET request to get the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the folder.
3. Make an HTTP POST request to the [loc:add-item](https://developer.avid.com/ctms/api/loc/linkrels/add-item.html) link with a JSON object with a property "base" with sub properties "systemType" (the  Avid Production Management type "avid-pmplus"), "systemID" (the ID of the  Avid Production Management), and "id" (the MOB ID of the asset to add) as body:

    ```
    {
    "base": {
        "systemType": "avid-pmplus",
        "systemID": "DD481E2E-260B-4684-9D25-44C774E3F782",
        "id": "060a2b340101010101010f0013-000000-070812007d070018-060e2b347f7f-d080"
    }
    }
    ```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Add asset to Folder (LinkToMob)/CTMS Add asset to folder (LinkToMob).postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

    <mark>🔶 At this step, you need to insert the appropriate **folder ID** in the environment variable named: folderIdInput</mark>

> **GET** 2_loc item resource of folder
- Hitting the above fetched selected_system_locItemByIdHref, to get the location/folder structure details of the selected folder ID.
- In the **Scripts** section: We fetch the "[loc:add-item](https://developer.avid.com/ctms/api/loc/linkrels/add-item.html)" link from the _links in the HAL output, and store it in selected_system_locAddItemHref variable globally.

> **POST** 3 add item
- We hit the selected_system_locAddItemHref link from above, that helps us to add the given asset to a given folder path.
- In the **Body** section: Add the asset information from "base" and "id" in the request body and send it along with the add item URL.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.