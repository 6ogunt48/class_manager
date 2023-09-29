#!/bin/sh
set -e

# Debugging: Echo the variables to make sure they are set as expected
echo "Debugging Variables:"
echo "HEROKU_REGISTRY_IMAGE: ${HEROKU_REGISTRY_IMAGE}"
echo "HEROKU_APP_NAME: ${HEROKU_APP_NAME}"
echo "HEROKU_AUTH_TOKEN: ${HEROKU_AUTH_TOKEN}"

# Fetch the Docker image ID
IMAGE_ID=$(docker inspect "${HEROKU_REGISTRY_IMAGE}" --format="{{.Id}}")
if [ -z "$IMAGE_ID" ]; then
  echo "Error: Couldn't fetch IMAGE_ID"
  exit 1
fi

# Prepare the payload for Heroku API
PAYLOAD="{\"updates\": [{\"type\": \"web\", \"docker_image\": \"${IMAGE_ID}\"}]}"

# Make the PATCH request to Heroku API
curl -X PATCH "https://api.heroku.com/apps/${HEROKU_APP_NAME}/formation" \
     -d "${PAYLOAD}" \
     -H "Content-Type: application/json" \
     -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
     -H "Authorization: Bearer ${HEROKU_AUTH_TOKEN}"

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "Error: Failed to update Heroku formation"
  exit 1
fi

echo "Successfully updated Heroku formation."
