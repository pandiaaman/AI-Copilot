# Documentation Title: Get Custom User Attributes

#### Summary:
The Interplay Web Services method GetCustomUserAttributes returns the registered user attributes for the  Avid Production Management workgroup.

## Get known attributes via CTMS

###### Steps:
1. Use the cached CTMS Registry information or fetch it as shown in Using the CTMS API.
2. Find the link [datamodel:system-model](https://developer.avid.com/ctms/api/datamodel/linkrels/system-model.html) for the  Avid Production Management and make an HTTP GET request to get the [datamodel:system-model](https://developer.avid.com/ctms/api/datamodel/linkrels/system-model.html) resource.

The property "attributes" lists the known attributes of the  Avid Production Management:

- "common" contains information about the common attributes. They are returned in the "common" property of assets ([aa:asset](https://developer.avid.com/ctms/api/aa/linkrels/asset.html) resource) and folders ([loc:item](https://developer.avid.com/ctms/api/loc/linkrels/item.html) resource).
- "custom" contains information about the raw user and system attributes of the  Avid Production Management. They are returned as property "attributes" for folders, and as property "attributes" in an embedded [aa:attributes](https://developer.avid.com/ctms/api/aa/linkrels/attributes.html) resource for assets, when requested with query parameter "?attributes=*" (to get all attributes) or "?attributes=a,b,c" (to get a comma-separated list of given attributes).

User attributes in  Avid Production Management are the ones with names that start with the prefix "com.avid.workgroup.Property.User".

#### How to use this collection:
This collection involves the process of following the above steps, as provided in the summary, in your postman application.
Open your postman, import the collection "Custom User Attributes/CTMS Get Custom User Attributes.postman_collection.json", and follow the steps as given below:

###### Postman API Calls
(Hit Send on the "ROPC Login" API call to login in the system. View the project-level ReadMe to understand how it works.)

> **GET** 1_CTMS Registry information: avid.ctms.registry
- This GET call hits the service roots URL for CTMS registry, fetching the resources, systems and the links associated to the system.
- In the **Scripts** section: We check if the  Avid Production Management is avaialable with the registry. If yes, we fetch "[datamodel:system-model](https://developer.avid.com/ctms/api/datamodel/linkrels/system-model.html)" link present inside the "resources", and store the variable globally as selected_system_dataModelSystemModelHref.

> **GET** 2 data model system model
- Hitting the above fetched selected_system_dataModelSystemModelHref, to get the custom user attributes in the output.
- In the **Params** section: You can set the parameter "attributes" as mentioned above in the summary tab.

#### Precautions/Recommendations:
- Please **select and put** the right asset/masterclip IDs in the environment required for this example.