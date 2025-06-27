import { readFileSync, stat } from "fs";

import path from 'path';

const cacheDir = path.join(__dirname, "..", "cache");
const data: string = readFileSync(path.join(cacheDir, "6899.pr.json"), "utf-8");
// const data: string = readFileSync(path.join(cacheDir, "6985.pr.json"), "utf-8"); // Draft
const validObj = JSON.parse(data);
const dataObj = validObj["data"];

if (dataObj["draft"]) {
    console.log("is draft, exiting");
    process.exit(1);
}

const authorName = dataObj["author"]["display_name"]
const participants = dataObj["participants"]
const validatedParticipants: any = [];
let validatedAuthor: any = [];

participants.forEach((participant: any) => {
    let approveCounter = 0;

    const state = participant.approved;
    const participantRole = participant.role;
    const userObj = participant.user;
    const name = userObj.display_name;
    const avatarLink = userObj.links.avatar.href;

    if (name === authorName) {
        validatedAuthor = {
            username: name,
            avatar: avatarLink,
        };
    } else {
        if(approveCounter == 2) {
            console.log("too much approves");
            process.exit(1);
        }

        if (state) {
            approveCounter++;
        } 

        validatedParticipants.push({
            approved: state,
            username: name,
            avatar: avatarLink,
        });
    }

});

const keys = ["state","reviewers", "type", "draft", "rendered", "merge_commit", "close_source_branch", "reason", "closed_by", "destination", "source", "links"]

keys.forEach(key => {
    delete dataObj[key]
});

dataObj["summary"] = dataObj["summary"]["html"]
dataObj["participants"] = validatedParticipants;
dataObj["author"] = validatedAuthor;

console.log(dataObj)