# Documentation Title: Reservations

## Add Reservations in CTMS

#### Summary:
The Interplay Web Services method AddReservation adds a new reservation to a given list of folders. The reservation can be created for an unlimited time or it can have an expiration time (given in seconds).

###### Parameter:
- The ID of the folder, consisting of the path with leading and trailing slashes. Example: "/Projects/Example/".
- Optional: an expiration date and time in ISO 8601 format. Example: "2024-05-15T14:40:35+00:00".

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API. 
2. Find the link loc:item-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template.
   1. Set the URI template variable "id" to the ID of the folder and expand the template.
   2. Add query parameter "?embed=reservations".
   3. Make an HTTP GET request to get the loc:item resource of the folder with an embedded protection:reservations resource. 
3. Call HTTP PUT on the embedded protection:set-reservation link with a JSON message body like this for a limited reservation:

```
   {
   "expiration": "2024-05-15T14:40:35+00:00"
   }
   Or for an unlimited reservation:
   {
   "expiration": null
   }
   
```
> To add a reservation to multiple folders, you must run steps 2 and 3 for each folder individually.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Reservations\CTMS Add Reservation.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> loc:item-by-id
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources" for "avid-pmplus" systemType, and store the variable globally as "selected_system_locItemByIdHref".
  Here we also replace "id" parameter in the url with user input "folder_path".

    <mark>🔶 At this step, you need to insert the appropriate **folder_path** in the environment variable.</mark>

> **Get** 2_loc:item-by-id -> protection:set-reservation
- Hitting the above fetched 'selected_system_locItemByIdHref', resource of the folder with an embedded protection:reservations resource. Here we need to pass embed='reservations' in query param.

- In the **Scripts** section: From the response, we fetch the "protection:set-reservation", which will be used to add reservation on a given folder, and store it globally as "selected_system_setReservationHref".

> **PUT** 3_Add Reservation
- Hitting the above selected_system_setReservationHref URL, to set the reservation on a folder,
- In the **Body** section: Add request body with the optional "expiration" field to add expiration date and time (if required) for the reservations to be added for the given folderId by hitting the PUT request.

#### Precautions/Recommendations:
- Please **select and put** the right **folder_id** or **folder_path** in the environment required for this example.

******

## Get Reservation

#### Summary:
The Interplay Web Services method GetReservations returns reservations on folders and assets.

  1. For a folder, it returns the reservations that are directly set on the folder, and reservations inherited from parent folders.
  2. For an asset reference in a folder, it can return either the reservations of that specific folder, including the inherited reservations, or it can return the combined reservations of all folders in the folder hierarchy that reference the asset, including the inherited reservations.
  3. For an asset referenced just by its MOB ID, it always returns the combined reservations of all folders in the folder hierarchy that reference the asset, including the inherited reservations.
  
  
###### Steps
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link loc:item-by-id for the  Avid Production Management. The "href" is an RFC-6570 URI template.
   1. Set the URI template variable "id" to the ID of the folder and expand the URI template.
   2. Add query parameter "?embed=reservations".
   3. Make an HTTP GET request to get the loc:item resource of the folder with an embedded protection:reservations resource containing information about the reservations on the folder.
 
Example for the embedded protection:reservations resource:
```
{
  "reservations": [
    {
      "creator": "svcadmin",
      "expiration": null,   // null means: reservation never expires
      "inherited": false
    },
    {
      "creator": "svcadmin",
      "expiration": "2024-05-17T14:15:52+00:00",
      "inherited": true
    }
  ]
}
```
> The reservations marked with "inherited": true are inherited from a parent folder.

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Reservations\CTMS Get Reservation.postman_collection.json", and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> loc:item-by-id
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available within the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources" for "avid-pmplus" systemType, and store the variable globally as "selected_system_folderItemByIdHref" for folder and "selected_system_assetItemByIdHref" for folder that contains asset.
  Here we also replace "id" parameter in the url with user input "folder_path" to get the reservation on a folder and "asset_path" to get the reservation on a folder that contains an asset.
  
    <mark>🔶 At this step, you need to insert the appropriate **folder_path** or **asset_path** in the environment variable. </mark>

> **GET** 2_Get reservation for a folder in CTMS
- Hitting the above fetched selected_system_folderItemByIdHref, to get the reservations for a folder by id.
- In the **Params** section: Enter the key value pairs as below:
    - embed: reservations
  
This will fetch you the reservations associated to the given folder in the response.

> **GET** 3_Get reservation for a folder that contains an asset.
- Hitting the above fetched selected_system_assetItemByIdHref, to get the reservations for a folder that contains an asset by assetId.
- In the **Params** section: Enter the key value pairs as below:
    - embed: reservations
- In the **Scripts** section: We fetch "[loc:referencing-items]" link present inside the [loc:referenced-object] in the embedded section. i.e, ["_embedded"]["loc:referenced-object"]["_links"]["loc:referencing-items"], and store the variable globally as "selected_system_referenceItemsHref" to fetch reservation on a referenced asset in subsequent collection.

This will fetch you the reservations for the folder that contains an asset in the response.

> **GET** 4_Get combined reservations of all folders that reference a given asset.
- Hitting the above fetched, "selected_system_referenceItemsHref" to get the reservations for all folders that reference a given asset.
- In the **Params** section: Enter the key value pairs as below:
    - embed: reservations
    - filter: item-type-all

This will fetch you combined reservations of all the folders that reference a given asset in the response. 
Response contains an embedded array of loc:item resources with all references to the asset in the entire folder hierarchy. Each loc:item resource has an embedded protection:reservations resource with the reservations on the folder. 

#### Precautions/Recommendations:
- Please **select and put** the right **folder_path or asset_path** in the environment required for this example.

******

## Remove Reservation

#### Summary:
The Interplay Web Services method RemoveReservations removes a direct reservation on a given list of folders. By default, it removes a reservation created by the caller. Optionally, you can remove the reservation that was created by a given user.


###### Steps

1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link loc:item-by-id for the  Avid Production Management. The "href" is an RFC-6570  URI template. 
   1. Set the URI template variable "id" to the ID of the folder and expand the URI template. 
   2. Add query parameter "?embed=reservations". 
   3. Make an HTTP GET request to get the loc:item resource of the folder with an embedded protection:reservation resource.
3. To delete the reservation that was created by the current user:
   1. Call HTTP DELETE on the protection:delete-reservation link.
4. To delete the reservation that was created by a given user:
   1. Find the protection:delete-reservation-by-creator link. The "href" is an RFC-6570  URI template. 
   2. Set the URI template variable "creator" to the username and expand the URI template. 
   3. Call HTTP DELETE on the resulting URI.


#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Reservations\CTMS Remove Reservation.postman_collection.json" and follow the steps as given below.

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_avid.ctms.registry -> loc:item-by-id
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is available with the registry. If yes, we fetch "[loc:item-by-id](https://developer.avid.com/ctms/api/loc/linkrels/item-by-id.html)" link present inside the "resources" for "avid-pmplus" systemType, and store the variable globally as "selected_system_locItemByIdHref".
  Here we also replace "id" parameter in the url with user input "folder_path".

- <mark>🔶 At this step, you need to insert the appropriate **folder_path** in the environment variable. </mark>

> **GET** 2_loc:item-by-id -> protection:delete-reservation
- Hitting the above fetched "selected_system_locItemByIdHref", to get the reservations for a folder by id.
- In the **Params** section: Enter the key value pairs as below:
    - embed: reservations
- In the **Scripts** section: We fetch ["protection:delete-reservation"] link present inside the embeded ["protection:reservations"] links for "avid-pmplus" systemType, and store the variable globally as "selected_system_removeReservationHref".

This will fetch you reservations of the given folder.
Response contains an embedded array of loc:item resources. Each loc:item resource has an embedded ["protection:reservations"] resource with the reservations on the folder.

> **DELETE** 3_Remove reservation
- Hitting the above fetched "selected_system_removeReservationHref", to remove the reservations for a given folder_path.
This will remove the reservations on the given folder path.
Response contains empty body with status code as '204 No content'.

#### Precautions/Recommendations:
- Please **select and put** the right **folder_path** in the environment required for this example.

