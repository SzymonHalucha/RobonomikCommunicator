function isWebSerialSupported() {
    return navigator.serial ? true : false;
}

async function addUSBDevice() {
    try {
        let device = await navigator.usb.requestDevice({ filters: [{}] });
        return {
            "ManufacturerName": device.manufacturerName,
            "SerialNumber": device.serialNumber,
            "DeviceName": device.productName,
            "DeviceId": device.productId,
            "VendorId": device.vendorId
        }
    } catch (error) {
        return {
            "ManufacturerName": "",
            "SerialNumber": "",
            "DeviceName": "",
            "DeviceId": 0,
            "VendorId": 0
        }
    }
}

async function getUSBDevicesList() {
    let list = await navigator.usb.getDevices();
    let devices = [];
    list.forEach(element => {
        devices.push({
            "ManufacturerName": element.manufacturerName,
            "SerialNumber": element.serialNumber,
            "DeviceName": element.productName,
            "DeviceId": element.productId,
            "VendorId": element.vendorId
        })
    });
    return devices;
}