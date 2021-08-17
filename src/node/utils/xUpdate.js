var MongoClient = require('mongodb').MongoClient;
var dbUrl = "mongodb://localhost:27017/";


function updateContent(category, items, key) {
    MongoClient.connect(dbUrl, function(err, db) {
        if (err) throw err;
        var dbo = db.db("pccomppicker");
        dbo.collection("products").find({"category": category}).project({title:1,_id:1}).toArray(function(err, result) {
            if (err) throw err;
            regexItem = items;
            for(j = 0;  j < result.length; j++) {
                for(i = 0;  i < regexItem.length; i++) {
                    let id = result[j]._id;
                    let regex = new RegExp(regexItem[i], "i");
                    let string = result[j].title;
                    let match = string.match(regex);
                    if(match != null && match[1] != undefined) {
                        match = match[1].toLowerCase();
                        match = match.replace(/\s/g,"");
                        query = { _id: id };
                        value = { $set: { [key]: match } };
                        dbo.collection("products").updateOne(query, value, function(err) {
                            if (err) throw err;
                            db.close();
                        });
                        break;
                    }
                }
            }
            db.close();
        });
    });
}

var category, key, category;

//**************CPU UPDATION******************//

category = "cpu";
key = "brand";
var cpu_brand = ['(amd)', '(intel)'];
updateContent(category, cpu_brand, key)

key = "series";
var cpu_series = ['(i\s?[3579])', '(ryzen\s?[3579])'];
updateContent(category, cpu_series, key)

//**************COOLER UPDATION****************/

category = "cooler";
key = "brand";
var cooler_brand = [
    '(adata)', '(aerocool)', '(ant\s?esports)', '(antec)', '(aorus)',
    '(arctic\s?silver)', '(arctic)', '(asus)', '(be\s?quiet)',
    '(cooler\s?master)', '(corsair)', '(deepcool)', '(ekwb)', '(enermax)',
    '(fractal\s?design)', '(gamdias)', '(gigabyte)', '(intel)', '(inwin)',
    '(jonsbo)', '(lian\s?li)', '(msi)', '(noctua)', '(nzxt)', '(pc\s?cooler)', 
    '(silverstone)', '(thermalright)', '(thermaltake)'
];
updateContent(category, cooler_brand, key)

var cooler_subcategory = [
    '(aio)', '[^s](air)', '(case fan)', '(gpu)', '(liquid)', '(paste)', '(cpu)', 
    '(radiator)', '(splitter)', '(tube)'
];
key = "sub category";
updateContent(category, cooler_subcategory, key)

//**************MOTHERBOARD UPDATION***********/

category = "motherboard";
key = "brand";

motherboard_brand = [
    '(aorus)', '(asrock)', '(asus)', '(biostar)', '(galax)', '(gigabyte)',
    '(msi)', '(nzxt)'
];
updateContent(category, motherboard_brand, key)

//**************MEMORY UPDATION***********/

category = "memory";
key = "brand";
memory_brand = [
    '(adata)', '(antec)', '(corsair)', '(crucial)', '(g\.skill)', '(gigabyte)',
    '(hyperx)', '(intel)', '(kingston)', '(klevv)', '(pny)', '(silicon\s?power)',
    '(supermicro)', '(team\s?group)', '(thermal\s?take)', '(zion)'
];
updateContent(category, memory_brand, key)

memory_type = ['(ddr[0-9])'];
key = "type";
updateContent(category, memory_type, key)

memory_capacity = ['([0-9]+\s?gb)'];
key = "capacity";
updateContent(category, memory_capacity, key)

memory_subcategory = ['(laptop)'];
key = "sub category";
updateContent(category, memory_subcategory, key)

memory_speed = ['([0-9]+\s?mhz)'];
key = "speed";
updateContent(category, memory_speed, key)

//**************STORAGE UPDATION***********/

category = "storage";
key = "brand";
storage_brand = [
    '(aorus)', '(astra)', '(asus)', '(corsair)', '(crucial)',
    '(dell)', '(galax)', '(gigabyte)',  '(hikvision)', '(intel)',
    '(kingston)', '(lexar)', '(pincoy)', '(pioneer)', '(pny)', '(samsung)',
    '(sandisk)', '(seagate)', '(silicon power)', '(teamgroup)', '(toshiba)',
    '(verbatim)', '(western\s?digital|wd)', '(xpg)', '(adata)', '(^h\s?p)',
];
updateContent(category, storage_brand, key)

key = "type";
storage_type= [ '(hdd)', '(m\.2)','(ssd)'];
updateContent(category, storage_type, key)

key = "capacity";
storage_capacity = ['([0-9]+\s?gb)|([0-9]+\s?tb)'];
updateContent(category, storage_capacity, key)

key = "form factor";
storage_formfactor = [ '(3\.5)', '(2\.5)'];
updateContent(category, storage_formfactor, key)

//**************CASE UPDATION*****************/

category = "case";
key = "brand";

case_brand = [
    '(adata)', '(aerocool)', '(ant\s?esports)', '(antec)', '(asus)', '(bitfenix)',
    '(chiptronex)', '(circle)', '(cooler\s?master)', '(corsair)', '(cougar)',
    '(deepcool)', '(fingers)', '(foxin)', '(fractal)', '(fractal\s?design)',
    '(gamdias)', '(gigabyte)', '(in\s?win)', '(jonsbo)', '(lian\s?li)',
    '(metallicgear)', '(montech)', '(msi)', '(nzxt)', '(phanteks)',
    '(silverstone)', '(thermaltake)', '(xpg)', '(zebronics)',
];
updateContent(category, case_brand, key)

//**************PSU UPDATION*****************/

category = "psu";
key = "brand";

psu_brand = [
    '(adata)', '(aerocool)', '(antec)', '(asus)', '(ant\s?esports)',
    '(antec)', '(circle)', '(cooler\s?master)', '(corsair)', '(deepcool)',
    '(fingers)', '(fractal\s?design)', '(fsp)', '(gigabyte)', '(gamdias)',
    '(msi)', '(nzxt)', '(phanteks)', '(seasonic)', '(silverstone)',
    '(super\s?flower)', '(seasonic)', '(silverstone)', '(thermal\s?take)',
    '(xpg)',
];
updateContent(category, psu_brand, key)

//**************GPU UPDATION*****************/

category = "gpu";
key = "brand";
gpu_brand = [
    '(asrock)', '(asus)', '(colorful)', '(cooler\s?master)',
    '(galax)', '(gigabyte)', '(inno3d)', '(msi)', '(nvidia)', '(nzxt)',
    '(palit)', '(pny)', '(power\s?color)', '(sapphire)', '(zotac)','(amd)'
];
updateContent(category, gpu_brand, key)

key = "series";
gpu_series = [ '(gtx)', '(rtx)', '(radeon)'];
updateContent(category, gpu_series, key)

//**************MONITOR UPDATION*****************/

category = "monitor";
key = "brand";

monitor_brand = [
    '(acer)', '(aoc)', '(aorus)', '(asus)', '(benq)', '(deepcool)',
    '(dell)', '(gigabyte)', '(^h\s?p)', '(^l\s?g)', '(lenovo)', '(msi)',
    '(philips)', '(phillips)', '(samsung)', '(viewsonic)', '(zowie)', '(amd)'
];
updateContent(category, monitor_brand, key)

key = "panel";
monitor_panel = ['(ips)', '(tn)', '(tft)', '(va)', '(lcd)', '(led)'];
updateContent(category, monitor_panel, key)
