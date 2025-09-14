# 📥 Importing and Configuring Postman Environment

To ensure a smooth and secure experience while using the provided Postman collections, follow the steps below to import and configure the Postman environment JSON file in your Postman application.

---

## ✅ Step 1: Import the Environment File

1. Open the **Postman** application.
2. In the left sidebar, click on the **"Environments"** tab (accessible via the gear icon ⚙️ at the top-right).
3. Click on the **"Import"** button.
4. Select the provided `default-env.postman_environment.json` file from your system.
5. Once imported, you will see the environment listed in your environments' dropdown.

---

## 🛠️ Step 2: Configure Required Variables

The imported environment contains a predefined set of variables required to interact with your on-premise system. These include:

- `mcs_user`  
- `mcs_password`  
- `mcs_host`

> ⚠️ **These variables are initially left empty. You must populate them before executing any collection.**

**Instructions:**
1. Click on the imported environment.
2. Enter your system’s specific values for:
   - `mcs_user`: Your username
   - `mcs_password`: Your password
   - `mcs_host`: Hostname or IP address of your CloudUX server
3. Save the environment.

---

## 🧾 Other Environment Variables

The environment also contains additional variables such as:

- `asset_id`
- `folder_id`
- `master_clip_id`
- `folder_path`
- `asset_path`, etc.

These are **system-specific** values and must be updated manually based on your available assets and folders.

You can discover these IDs using:
- The **CloudUX interface**
- Postman API calls (e.g., `CTMS Service Provider` collection)

> 🔶 The collection-specific documentation will indicate exactly where and which variable you need to populate.  
> For example:  
> "At this step, you need to insert the appropriate Asset ID in the environment variable named: `asset_id`"

---

## 📂 Recommended Practice

To ensure a safe and controlled environment:

- **Create a dedicated test folder** in your system.
- Use this folder to create or duplicate assets for testing purposes.
- Reference the IDs of these assets/folders when running destructive operations (e.g., delete, update).

This minimizes the risk of accidentally modifying or deleting production content.

---

## 🚫 Important Cautions

- **Do not run collections before configuring `mcs_user`, `mcs_password`, and `mcs_host`** — authentication will fail.
- Avoid using production asset/folder IDs unless you are certain of the operation.
- Always review pre-filled variables before executing operations such as delete, reserve, or modify.

---

By properly configuring your environment and understanding the responsibilities around variable management, you ensure secure and accurate execution of CTMS API workflows within your own system.