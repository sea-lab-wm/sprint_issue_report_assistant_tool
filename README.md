BEE_v2 tool for bug report duplicate detection, severity prediction and bug localization

## Download the Models 
[models](https://drive.google.com/drive/folders/1IQdWRwUKVGmU-8p4PNbWd4vTxIAuaoNY?usp=sharing)


## How to Run the Tool
### If the tool is deployed

Step 1: Just install the plugin in a specific Github repository and the tool will work on that repository


## Manually run the tool

**Step 1:** 

Clone the repository 


**Step 2:**

Install [ngrok] from (https://ngrok.com/download) [This will create a secure tunnel from a public endpoint (Github repository) to a locally running network service (our project running in localhost)]


**Step 3:** 

Generate a private access token (this token will enable permission for our tool to fetch and post data to a user’s Github repositories). Make sure in ‘Repository Permissions’ section, there is Read and Write access to ‘Actions’, ‘Webhooks’ and ‘Issues’.

   Profile -> Settings -> Developer Settings -> Personal Access Tokens -> Fine-grained Tokens -> Generate New Token

After generating the token, copy and paste it to the cloned project’s .env file
(in GITHUB_PRIVATE_KEY variable)


**Step 4:**

Open the cloned project in IDE and run the following 2 commands in 2 different terminals -

`./ngrok http 5000`

python main.py



**Step 5:**

Go to the repository where you need to run the tool. Go to -

Settings -> Webhooks -> Add Webhook 

Then copy the forwarding address shown after running the command ‘ ./ngrok http 5000 ’ into the Payload URL section of Add Webhook. 




Make sure ‘Which events would you like to trigger this webhook?’ section has ‘Issues’, ‘Issue Comments’ and ‘Labels’ checkboxes checked



**Step 6:**

Create issues in that repository and see the tool work

