
export function makeId(length = 5) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
export function convertDateToUTC(date,time=0){
    const dates= date.split("-")
    const times=time.split(":")
    return Date.UTC(dates[0],dates[1],dates[2],times[0],times[1]);
}
