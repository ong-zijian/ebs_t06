# ebs_t06

## Current Image:
current version of the image: smuozj/ebst06backend:v1.5

## Deployment Steps:
- Edit the `deployment.yaml` image details if there is a new image
- Go to command prompt in the root directory and run (insert the api key on the "apikey" part)
`kubectl create secret generic openai-secret--from-literal=OPENAI_KEY="apikey"`
- Use the set context: `kubectl config set-context --current --namespace=smu-team06`
- Check if you can see the pods: `kubectl get pods`
- Run the command to deploy the kubernetes `kubectl apply -f ./deployment.yaml`

## Run steps:
### Simple Hello World test route
Use postman or even web browser for this.
`https://smu-team06-api.ede20ab.kyma.ondemand.com/`

### Emotion detection
- Go to Postman, use the `POST` method
- insert this to the url `https://smu-team06-api.ede20ab.kyma.ondemand.com/mood`
- for the body, select `raw`, then `JSON` and insert below, or use any text you like:
`
{
    "mood":"Today was a terrible day."
}
`



