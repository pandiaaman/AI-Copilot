# Documentation Title: Move Item

#### Summary:
The Interplay Web Services method Move moves an asset from a source folder to a target folder, or an entire folder to a target folder. If a sequence is moved, the referenced assets are also moved (or copied if they are referenced by another sequence in the source folder) to the target folder.

The method allows overriding reservations if needed.

## Move an asset or folder to a target folder in CTMS

###### Parameter:
- The ID of the item to move:
    - For an asset: the path to the asset with a leading "/". The last path element is the MOB ID. Example: "/Catalogs/IPWS/060a2b340101010101010f0013-000000-070812007d070018-060e2b347f7f-d080"
    - For a folder: the path with leading and trailing slashes. Example: "/Catalogs/IPWS/".
- The ID of the target folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html) for the  Avid Production Management. The "href" is an  URI template.
    - Set the URI template variable "id" to the ID of the target folder and expand the URI template.
    - Make an HTTP GET request to get the [loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource of the folder.
3. Find the [loc:move-item](https://developer.avid.com/ctms/api/loc/linkrels/move-item.html) link.
    - If you want to override reservations, set the query parameter "override-reservations" to "all".
    - Make an HTTP POST call with a JSON object in the request body with a property "base" with the sub properties:
        - "systemType": the  Avid Production Management type "avid-pmplus".
        - "systemID": the ID of the  Avid Production Management.
        - "type": "folder" for a folder, and "folder-item" for an asset.
        - "id": the path to the asset or folder.

    Example: 

    ```
    {
    "base": {
        "systemType": "avid-pmplus",
        "systemID": "DD481E2E-260B-4684-9D25-44C774E3F782",
        "type": "folder-item",
        "id": "/Catalogs/IPWS/060a2b340101010101010f0013-000000-070812007d070018-060e2b347f7f-d080"
    }
    }
    ```

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Move Item/CTMS Move Item.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources", and store the variable globally as selected_system_locItemByIdHref.

> **GET** 2_loc item by id
- Hitting the above fetched selected_system_locItemByIdHref, to get the loc item by id which represents the location of the item.
- In the **Scripts** section: From the response, we fetch the "[loc:move-item](https://developer.avid.com/ctms/api/loc/linkrels/move-item.html)", which is used to get the link to move an item, and store it globally as selected_system_locMoveItem.

> **POST** 3_create Folder Inside Desired Location
- Hitting the above selected_system_locMoveItem URL, to move the item to the desired location.
- In the **Body** section: We put the "base" information of the item that we want to move, as defined above in the summary tab.

    <mark>🔶 At this step, you need to insert the appropriate **systemType, systemID, type and id** in the "base" section of the request body that we are sending.</mark>

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.
- Please make sure to use the correct item id, type etc., in the request body at step 3.