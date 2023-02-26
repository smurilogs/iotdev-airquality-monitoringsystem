
function decodeUplink(input) {
    
    var data = {};
    var warnings = [];

    if (input.fPort == 10) {
        data.temp = ((input.bytes[0] << 8) + input.bytes[1]) 
            + (((input.bytes[2] << 8) + input.bytes[3])/100.0);
        
        data.rh = ((input.bytes[4] << 8) 
        + input.bytes[5]) + (((input.bytes[6] << 8)
            + input.bytes[7])/100.0);
        
        data.pm1_0 = ((input.bytes[8] << 8) | input.bytes[9]);
        data.pm2_5 = ((input.bytes[10] << 8) | input.bytes[11]);
        data.pm10_0 = ((input.bytes[12] << 8) | input.bytes[13]);
    }
    else {
        warnings.push("Unsupported fPort");
    }
    return {
        data: data,
        warnings: warnings
    };
}
    