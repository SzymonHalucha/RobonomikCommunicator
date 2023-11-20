function isWebUSBSupported() {
    return navigator.usb ? true : false;
}

async function addDevice() {
    try {
        let device = await navigator.usb.requestDevice({ filters: [] });
        return {
            "ManufacturerName": device.manufacturerName,
            "ProductName": device.productName,
            "ProductId": device.productId,
            "VendorId": device.vendorId
        }
    } catch (error) {
        return {
            "ManufacturerName": "Empty",
            "ProductName": "Empty",
            "ProductId": -1,
            "VendorId": -1
        }
    }
}

async function getDevicesList() {
    let list = await navigator.usb.getDevices();
    let devices = [];
    list.forEach(element => {
        devices.push({
            "ManufacturerName": element.manufacturerName,
            "ProductName": element.productName,
            "ProductId": element.productId,
            "VendorId": element.vendorId
        })
    });
    return devices;
}