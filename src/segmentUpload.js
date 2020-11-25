// dependencies
var async = require('async');
const fs = require('fs');
const path = require('path');

// csvtojson quickly and easily parses and formats our CSV files
var csv = require('csvtojson');
// the following are Segment libraries
var Analytics = require('analytics-node');
var Objects = require('objects-node');

const dotenv = require('dotenv');
dotenv.config();
var analytics = new Analytics(process.env.write_key);
var objects = new Objects(process.env.write_key);



const sendToSegment = function(callback, srcFileName) {
    // Read options from the event.
    //console.log("Reading options from event:\n", util.inspect(event, {depth: 5}));
    // File name may have spaces or unicode non-ASCII characters.
    // Download the CSV from S3, transform, and upload to Segment.
    // More on async.waterfall here: https://caolan.github.io/async/docs.html#waterfall

    async.waterfall([
        function download(next) {
            // Download the CSV from S3 into a buffer.
            var filePath = '../to-save/'+ new Date().toLocaleDateString().replace(/\//g, '-').slice(0,-2) + '/' + srcFileName
            console.log(filePath) 
            const data = fs.readFileSync(path.resolve(__dirname, filePath))
            next(null,data.toString())
        },
        function transform(csvString , next) {
            console.log("transform");
            //console.log(csvString)
            // In colParser we ensure that our timestamps aren't strings, Segment APIs don't like strings here
            csv({
            	colParser:{
            		"createdAt":function(item){return new Date(item);},
                "timestamp":function(item){return new Date(item);},
            	}
            })
            .fromString(csvString)
            .then((formattedResults)=>{
              next(null,formattedResults);
            })
        },
        function upload(formattedResults, next) {
            //console.log("upload");
            if(srcFileName.includes('identify')){
              formattedResults.map(function(identifyObject){
                // More in the docs here: https://segment.com/docs/connections/spec/identify/
                analytics.identify(identifyObject)
              });
            }else if(srcFileName.includes('track')){
              formattedResults.map(function(trackObject){
                // More in the docs here: https://segment.com/docs/connections/spec/track/
                analytics.track(trackObject);
              });
            }else if(srcFileName.includes('page')){
              formattedResults.map(function(pageObject){
                // More in the docs here: https://segment.com/docs/connections/spec/page/
                analytics.page(pageObject);
              });
            }else if(srcFileName.includes('screen')){
              formattedResults.map(function(screenObject){
                // More in the docs here: https://segment.com/docs/connections/spec/screen/
                analytics.screen(screenObject);
              });
            }else if(srcFileName.includes('group')){
              formattedResults.map(function(groupObject){
                // More in the docs here: https://segment.com/docs/connections/spec/group/
                analytics.group(groupObject);
              });
            }else if(srcFileName.includes('alias')){
              formattedResults.map(function(aliasObject){
                // More in the docs here: https://segment.com/docs/connections/spec/alias/
                analytics.alias(aliasObject);
              });
            }else if(srcFileName.includes('object')){
              // Who doesn't love a variable named objectObject?! :(
              formattedResults.map(function(objectObject){
                // The Object API accepts a different format than the other APIs
                // More in the docs here: https://github.com/segmentio/objects-node
                // First, we get our collection name
                var objectCollection = srcFileName.split("_")[1];
                // Then, we get and delete our objectId from the object we pass into Segment
                var objectId = objectObject.id;
                delete objectObject.id;
                console.log("objectCollection: ",objectCollection);
                console.log("objectId: ", objectId);
                console.log("objectObject: ",objectObject);
                objects.set(objectCollection, objectId, objectObject);
              });
            }else{
              console.log("ERROR! No call type specified! Your CSV file in S3 should start with 'identify_', 'track_', 'page_', 'screen_', 'group_', 'alias_' or 'object_<collection>'");
              throw new Error;
            }
            // Now we make sure that all of our queued actions are flushed before moving on
            if(srcFileName.startsWith('object_')){
              var objectCollection = srcFileName.split("_")[1];
              objects.flush(objectCollection, function(err, batch){
                next(err,"Done");
              });
            }else{
              analytics.flush(function(err, batch){
                console.log(srcFileName + ' Flushed, and now this program can exit!');
            });
            }
        }
      ], function (err) {
            // Some pretty basic error handling
            if (err) {
                console.error(
                    'Unable to download ' + srcBucket + '/' + srcFileName +
                    ' and upload to Segment' +
                    ' due to an error: ' + err
                );
            } else {
                console.log(
                    'Successfully downloaded ' + srcBucket + '/' + srcFileName +
                    ' and uploaded to Segment!'
                );
            }
            callback(null, "Success!");
        }
    );
};

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

var files = fs.readdirSync(`/Users/isaacrenner/Documents/automation/autoUpload/to-save/${new Date().toLocaleDateString().replace(/\//g, '-').slice(0,-2)}/` );
files.forEach(file => 
    {
        if(file.includes('Segment')){
            sleep(60000)            
            console.log(file)
            sendToSegment((data)=> (data) , file);
        }
    }
)
