const fs = require('fs');
var myArgs = process.argv.slice(2);
const xsdFile = myArgs[0];
const xsdObjectFile = myArgs[1];
//
const complexTypeStartTag = "<xsd:complexType"
const elementStartTag = "<xsd:element"
// Log arguments
console.log('myArgs: ', myArgs);
console.log('xsd: ', xsdFile);
//
// Exctract an attribute value from an element
function getAttributeValue(element, attributeName) {
    var attribute = ""
    var attributePos = element.indexOf(attributeName);
    if (attributePos >  - 1) {
        attribute = element.substring(attributePos);
        attributePos = attribute.indexOf("=") + 1;
        attribute = attribute.substring(attributePos).trim();
        var enclosingChar = attribute.substring(0, 1);
        attribute = attribute.substring(1, attribute.indexOf(enclosingChar, 1));
    }
    return attribute;
}

function writeXSDObjects(listOfObjects) {
    // Create complexType Output file.
    console.log("Write XSD Objects to file...")
    //fs.writeFileSync(xsdObjectFile, "Nr,Type,Name\n");
    fs.writeFile(xsdObjectFile, 'Nr,Type,Name\n', function (err) {
        if (err)
            throw err;
        for (var idx = 0;idx < listOfObjects.length;idx++) {
            var object = listOfObjects[idx];
            var line = "";
            line = line.concat(object.nr.toString(), ",", object.type, ",", object.name, "\n")
            fs.appendFileSync(xsdObjectFile, line);
            //console.log(line);
        }
    });
}

/** Function that count occurrences of a substring in a string;
 * @param {String} string               The string
 * @param {String} subString            The sub string to search for
 * @param {Boolean} [allowOverlapping]  Optional. (Default:false)
 *
 * @author Vitim.us https://gist.github.com/victornpb/7736865
 * @see Unit Test https://jsfiddle.net/Victornpb/5axuh96u/
 * @see http://stackoverflow.com/questions/4009756/how-to-count-string-occurrence-in-string/7924240#7924240
 */
function occurrences(string, subString, allowOverlapping) {
    string += "";
    subString += "";
    if (subString.length <= 0)
        return (string.length + 1);

    var n = 0, pos = 0, step = allowOverlapping ? 1 : subString.length;

    while (pos >= 0) {
        pos = string.indexOf(subString, pos);
        if (pos >= 0) {
            ++n;
            pos += step;
        }
    }
    return n;
}

function getXsdNextObject(contents, startPos, xsdObjectType) {
    var xsdObjectStartTag = "<xsd:".concat(xsdObjectType)
    var xsdObjectEndTag = "<\/xsd:".concat(xsdObjectType)
    var posStartXsdObject = contents.indexOf(xsdObjectStartTag, startPos);
    var posEndXsdObjectDecl = contents.indexOf(">", posStartXsdObject) + 1;
    var xsdObjectDecl = contents.substring(posStartXsdObject, posEndXsdObjectDecl);
    console.log("xsdObject Declaration: ", "[".concat(xsdObjectDecl, "]"));
    var posEndXsdObject = posEndXsdObjectDecl;
    // Check if it is an empty element tag.
    if (!xsdObjectDecl.endsWith("/>")) {
        //Not an empty element tag.        
        posEndXsdObject = contents.indexOf(xsdObjectEndTag, posEndXsdObject + 1);
        posEndXsdObject = contents.indexOf(">", posEndXsdObject) + 1;
        var xsdObjectStr = contents.substring(posStartXsdObject, posEndXsdObject);
        //var countXsdObjectStarts = (xsdObject.match(/<xsd:/g) || []).length;
        //var countXsdObjectEnds = (xsdObject.match(/<\/xsd:/g) || []).length;
        var countXsdObjectStarts = occurrences(xsdObjectStr, xsdObjectStartTag);
        var countXsdObjectEnds = occurrences(xsdObjectStr, xsdObjectEndTag);
        console.log("Start and end tags: ", "".concat(countXsdObjectStarts, "-", countXsdObjectEnds));
        while (countXsdObjectStarts != countXsdObjectEnds) {
            posEndXsdObject = contents.indexOf(xsdObjectEndTag, posEndXsdObject);
            posEndXsdObject = contents.indexOf(">", posEndXsdObject) + 1;
            xsdObjectStr = contents.substring(posStartXsdObject, posEndXsdObject);
            countXsdObjectStarts = occurrences(xsdObjectStr, xsdObjectStartTag);
            countXsdObjectEnds = occurrences(xsdObjectStr, xsdObjectEndTag);
            console.log("Start and end tags: ", "".concat(countXsdObjectStarts, "-", countXsdObjectEnds));
        }
    }
    //console.log("xsdObject: ", "[".concat(xsdObjectStr, "]"));
    //Create xsdObject 
    var xsdObject = {
    }
    xsdObject['type'] = xsdObjectType;
    xsdObject['name'] = getAttributeValue(xsdObjectDecl, "name");;
    xsdObject['startPos'] = posStartXsdObject;
    xsdObject['endPos'] = posEndXsdObject;
    return xsdObject;
}
// Read and process the xsdFile
fs.readFile(xsdFile, 'utf8', function (err, contents) {
    var listOfObjects = [];
    var nr = 0;
    //Handle Elements and ComplexTypes
    var xsdTagStartPos = contents.indexOf("<xsd:", 0);
    while (xsdTagStartPos >= 0) {
        var xsdTagEndPos = contents.indexOf(">", xsdTagStartPos) + 1;
        var xsdTag = contents.substring(xsdTagStartPos, xsdTagEndPos);
        var xsdObject = null
        console.log("xsdTag: ", "[".concat(xsdTag, "]"));
        if (xsdTag.startsWith("<xsd:complexType")) {
            xsdObject = getXsdNextObject(contents, xsdTagStartPos, "complexType");
            xsdObject['nr'] = ++nr;
            listOfObjects.push(xsdObject);
            console.log(console.table(xsdObject));
            xsdTagEndPos = xsdObject.endPos + 1;
        }
        else {
            if (xsdTag.startsWith("<xsd:element")) {
                xsdObject = getXsdNextObject(contents, xsdTagStartPos, "element");
                xsdObject['nr'] = ++nr;
                listOfObjects.push(xsdObject);
                console.log(console.table(xsdObject));
                xsdTagEndPos = xsdObject.endPos + 1;
            }
        }
        xsdTagStartPos = contents.indexOf("<xsd:", xsdTagEndPos);
        console.log("xsdTagStartPos: ", xsdTagStartPos);
    }
    writeXSDObjects(listOfObjects);
});
//
console.log('Done with ' + xsdFile);