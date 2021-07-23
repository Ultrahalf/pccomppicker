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
var cpu_series = ['(i.?[0-9])', '(ryzen.?[0-9])'];
updateContent(category, cpu_series, key)

//**************COOLER UPDATION****************/

category = "cooler";
key = "brand";
var cooler_brand = [
    '(adata)', '(aerocool)', '(ant.?esports)', '(antec)', '(aorus)',
    '(arctic.?silver)', '(arctic)', '(asus)', '(be.?quiet)',
    '(cooler.?master)', '(corsair)', '(deepcool)', '(ekwb)', '(enermax)',
    '(fractal.?design)', '(gamdias)', '(gigabyte)', '(intel)', '(inwin)',
    '(jonsbo)', '(lian.?li)', '(msi)', '(noctua)', '(nzxt)', '(pc.?cooler)', 
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
    '(hyperx)', '(intel)', '(kingston)', '(klevv)', '(pny)', '(silicon.?power)',
    '(supermicro)', '(team.?group)', '(thermal take)', '(thermaltake)', '(zion)'
];
updateContent(category, memory_brand, key)

memory_type = ['(ddr[0-9])'];
key = "type";
updateContent(category, memory_type, key)

memory_capacity = ['([0-9]+.?gb)'];
key = "capacity";
updateContent(category, memory_capacity, key)

memory_subcategory = ['(laptop)'];
key = "sub category";
updateContent(category, memory_subcategory, key)

memory_speed = ['([0-9]+.?mhz)'];
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
    '(verbatim)', '(western digital|wd)', '(xpg)', '(adata)', '(\sh.?p)',
];
updateContent(category, storage_brand, key)

key = "type";
storage_type= [ '(hdd)', '(m\.2)','(ssd)'];
updateContent(category, storage_type, key)

key = "capacity";
storage_capacity = ['([0-9]+.?gb)|([0-9]+.?tb)'];
updateContent(category, storage_capacity, key)

key = "form factor";
storage_formfactor = [ '(3\.5)', '(2\.5)'];
updateContent(category, storage_formfactor, key)

//**************CASE UPDATION*****************/

category = "case";
key = "brand";

case_brand = [
    '(adata)', '(aerocool)', '(ant.?esports)', '(antec)', '(asus)', '(bitfenix)',
    '(chiptronex)', '(circle)', '(cooler.?master)', '(corsair)', '(cougar)',
    '(deepcool)', '(fingers)', '(foxin)', '(fractal)', '(fractal.?design)',
    '(gamdias)', '(gigabyte)', '(in.?win)', '(jonsbo)', '(lian.?li)',
    '(metallicgear)', '(montech)', '(msi)', '(nzxt)', '(phanteks)',
    '(silverstone)', '(thermaltake)', '(xpg)', '(zebronics)',
];
updateContent(category, case_brand, key)

//**************PSU UPDATION*****************/

category = "psu";
key = "brand";

psu_brand = [
    '(adata)', '(aerocool)', '(antec)', '(asus)', '(ant.?esports)',
    '(antec)', '(circle)', '(cooler master)', '(corsair)', '(deepcool)',
    '(fingers)', '(fractal.?design)', '(fsp)', '(gigabyte)', '(gamdias)',
    '(msi)', '(nzxt)', '(phanteks)', '(seasonic)', '(silverstone)',
    '(super.?flower)', '(seasonic)', '(silverstone)', '(thermal.?take)',
    '(xpg)',
];
updateContent(category, psu_brand, key)

//**************GPU UPDATION*****************/

category = "gpu";
key = "brand";
gpu_brand = [
    '(asrock)', '(asus)', '(colorful)', '(cooler.?master)',
    '(galax)', '(gigabyte)', '(inno3d)', '(msi)', '(nvidia)', '(nzxt)',
    '(palit)', '(pny)', '(power.?color)', '(sapphire)', '(zotac)','(amd)'
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
    '(dell)', '(gigabyte)', '(h.?p)', '(l.?g)', '(lenovo)', '(msi)',
    '(philips)', '(phillips)', '(samsung)', '(viewsonic)', '(zowie)', '(amd)'
];
updateContent(category, monitor_brand, key)

key = "panel";
monitor_panel = ['(ips)', '(tn)', '(tft)', '(va)', '(lcd)', '(led)'];
updateContent(category, monitor_panel, key)
