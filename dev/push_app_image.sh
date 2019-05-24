#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR=$(dirname "${DIR}")

source "${DIR}/common.sh"

echo "Root directory is ${ROOT_DIR}"
pushd "${ROOT_DIR}"
  # Set via `travis env set DOCKER_USERNAME username`
  echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USERNAME}" --password-stdin
  echo "Getting current app image tag"
  TAG=$(get_current_tag)
  IMAGE_NAME="bmwant/bmwlog:${TAG}"
  echo -e "Current tag: ${TAG}\nImage: ${IMAGE_NAME}"

  NOT_PRESENT=$(check_image_exists ${IMAGE_NAME})
  if [[ ${NOT_PRESENT} -eq 0 ]]; then
    echo "Image already exists, nothing to push"
    exit 0
  fi

  echo "Pushing app docker image"
  docker push ${IMAGE_NAME}
  # Retag image as latest
  LATEST_IMAGE_NAME="bmwant/bmwlog:latest"
  docker tag ${IMAGE_NAME} ${LATEST_IMAGE_NAME}
  docker push ${LATEST_IMAGE_NAME}
 popd
