
[TOC]

# OVA Overview

The OVA controller should be configured like any other linux program. through config files. This should feel seamless.

OVA controller is split in three sub-projects.

### Controller

} Controls, tracks and manages the states of accessories. It can be updated and configured via the API.

### Accessory Interface
	
} Used by any device connected to the local AP to update the state of the accessories controlled by the controller.
} This is a webpage with javascript request that talk to the controller's API.

### Controller Config Interface

} Used by privileged devices (mac or ip address?) to configure the Accessories. For example the head unit or a laptop plugged into the pi.
	
} Devices connected via the `usb0` interface automatically become privileged.


# API V1 Objects

## Accessory

- `"id":string` the unique identifer of an accessory.
- `"name":string` the friendly name of this accessory shown in the user interface.
- `"icon":url` the url to the icon used in conjunction with the name.
- `"controller":controller-id` the unique identifer of the controller used for this accessory.
- `"parameters":object` the parameters for the controller used on this accessory.

The accessory should be stored in plaintext as a json file on local storage. The filename should have the id directly followed by the json extension (`my-accessory.json`).

This is to allow users to view (and modify) the configuration of accessories without having to use the API or a web interface.

However the state is managed by the controller. It's the controller's job to manage and track the state of the accessory.

## IDs

An "id" must be human readable and safe for computer storage. Therefore can only contain a-z, 0-9 and `-` (hyphen).

A good example would be `spotlights-2` or `relay-h-bridge`. A bad example would be `🔥FIRE_suppression` or `Ejector Seat!`

# API V1 Endpoints

## `GET /about`

Get detailed information about this controller.

### Response

- `200 OK` on success
```json
{
	"ova":
	{
		"version": "0.1.4 beta",
		"date": 2020-04-26,
		"serial": "dev-3f4",
		"hostname": "ova-controller",
	},
	"access-point":
	{
		"qr-code": "/ova/wifi-qr.png",
		"ssid": "toms-zook.ova",
		"password": "q7f-rz2-6af"
	},
	"vehicle":
	{
		"nickname": "Tom's Zook",
		"make": "Suzuki",
		"model": "Vitara",
		"fitted": "Fitted by God himself."
	}
}
```

## `GET /accessories`

List all the accessories currently configured with this ova-controller.

### Response

- `200 OK` on success
```json
[
	{
		"id": "compressor",
		"name": "Air Compressor",
		"icon": "/ova/icons/default/compressor.svg",
		"type": "relay",
		"controller":
		{
			"state": "on",
			"output": 2
		}
	},
	{
		"id": "driver-window",
		"name": "Driver Electric Window",
		"icon": "/ova/icons/default/window.svg",
		"controller": "relay-h-bridge",
		"parameters":
		{
			"state": "off",
			"forward-output": 4,
			"reverse-output": 5,
		}
	},
]
```

## `GET /accessories/{id}`

Get a singular accessory with the specified id.

## Arguments
- `{id}` the uid of an accessory.

## Response

- `200 OK`
```json
{
	"id": "driver-window",
	"name": "Driver Electric Window",
	"icon": "/ova/icons/default/window.svg",
	"controller": "relay-h-bridge",
	"parameters":
	{
		"state": "off",
		"forward-output": 4,
		"reverse-output": 5,
	}
},
```
- `404 Not Found` the id does not exist.

## `PUT /accessories`

Creates a new accessory.

### Arguments

- `"id":string` a globally unique identifier for this accessory.
- `"name":string` a friendly name used in the user interfaces.
- `"icon":string` a URL to the icon used in the user interfaces.
- `"controller":string` the controller that controls this accessory.
- `"parameters":string` the parameters for this controller.

### Response

- `201 Created` the accessory has been created.
- `400 Bad Request` the request did not contain valid arguments.
- `401 Unauthorized` the accessory/gpio is in use.
- `409 Conflict` the id has conflicted with another id.


## `DELETE /accessories/{id}`

Delete an accessory with the provided id.

### Arguments
- `{id}` the uid of an accessory.

### Response

- `204 No Content` the accessory was deleted.
- `401 Unauthorized` the accessory/gpio is in use.
- `404 Not Found` the id does not exist.


## `POST /accessories/{id}`

Add update an existing accessory with the provided id.

### Arguments
- `{id}` the uid of an accessory.
- `"name":string` a friendly name used in the user interfaces.
- `"icon":string` a URL to the icon used in the user interfaces.

### Response

- `204 No Content` the accessory has been updated.
- `404 Not Found` the id does not exist.


## `GET /accessories/{id}/state`

Get the sate of an accessory. The state is provided by the controller and varies from controller to controller.

### Arguments
- `{id}` the uid of an accessory.

### Response

- `200 OK`
	
	**[ Changes per controller! ]**
- `404 Not Found` the id does not exist.


## `POST /accessories/{id}/state`

Set the sate of an accessory. The state is provided by the controller and varies from controller to controller.

### Arguments

- `{id}` the uid of an accessory.
**[ Changes per controller! ]**

### Response

- `204 No Content` the accessory's state has been changed.
- `404 Not Found` the id does not exist.


