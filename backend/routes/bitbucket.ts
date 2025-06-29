// Imports
import express, { Request, response, Response } from "express";
import axios from "axios";
import dotenv from "dotenv";
import fs from "fs/promises";
import * as fsSync from 'fs';
import path from "path";

dotenv.config();

// Variables
const router = express.Router();


// Interfaces:
interface BitbucketMainResponse {
  values: PullRequest[];
  pagelen: number;
  size: number;
  page: number;
}

interface PullRequest {
  comment_count: number;
  task_count: number;
  type: string;
  id: number;
  title: string;
  description: string;
  state: string;
  draft: boolean;
  merge_commit: null | unknown;
  close_source_branch: boolean;
  closed_by: null | unknown;
  author: Author;
}

interface Author {
  display_name: string;
  links: AuthorLinks;
  type: string;
  uuid: string;
  account_id: string;
  nickname: string;
}

interface AuthorLinks {
  self: { href: string };
  avatar: { href: string };
  html: { href: string };
}

interface ModificationCheck {
  was_modified: boolean;
  last_modified: Number;
}

// Helper Functions
async function getCache(endpoint: string): Promise<BitbucketMainResponse | any> {
  const username = process.env.API_USER;
  const apiKey = process.env.API_KEY;

  if (!username || !apiKey) {
    throw new Error("API_USER and API_KEY must be defined in environment variables");
  }

  const reqObject = {
    auth: {
      username,
      password: apiKey,
    },
    headers: {
      Accept: "application/json",
    },
    params: {
      pagelen: 50,
    },
  };

  try {
    const response = await axios.get(endpoint, reqObject);
    return response.data;
  } catch (e) {
    console.log(e);
    throw e;
  }
}

function buildUrl(...params: string[]): string {
  const parts = ["https://api.bitbucket.org/2.0"];

  for (const param of params) {
    // Replace all "/" chars
    const cleanPart = param.replace(/^\/+|\/+$/g, "");
    parts.push(cleanPart);
  }

  return parts.join("/");
}

async function saveJSON(data: any, filePath: string): Promise<void> {
  await fs.writeFile(
    filePath,
    JSON.stringify({ data }, null, 2),
    "utf-8"
  );
}

function getCacheFolder(): string {
  const rootDir = process.env.ROOT_DIR ?? path.join(__dirname, "..");
  return path.join(rootDir, "cache");
}

function wasModifiedWithinLastHour(filePath: string): ModificationCheck {
  try {
    const stats = fsSync.statSync(filePath);
    const lastModified = stats.mtime;
    const oneHourAgo = Date.now() - 3600 * 1000;
    return {
      was_modified: lastModified.getTime() < oneHourAgo,
      last_modified: lastModified.getTime(),
    };
  } catch (err) {
    console.error("Error reading file stats:", err);
    return {
      was_modified: false,
      last_modified: 0,
    };
  }
}

function fileExists(filePath: string): boolean {
  try {
    fsSync.accessSync(filePath);
    return true;
  } catch {
    return false;
  }
}

// Routes
router.post("/reload-cache", async (req: Request, res: Response<{ success: boolean; message: string }>): Promise<any> => {
  const masterCacheFile = path.join(getCacheFolder(), "pullRequestIds.json");
  if (fileExists(masterCacheFile)) {
    const modificationObj = wasModifiedWithinLastHour(masterCacheFile);
    if (modificationObj.was_modified) {
      return res.status(200).json({ success: true, message: "Cache was updated withing last hour" });    
    }
  }
  
  const project = process.env.PROJECT;
  const organization = process.env.ORGANIZATION;

  if (!project || !organization) {
    throw new Error("PROJECT and ORGANIZATION must be defined in environment variables");
  }

  try {
    const endpoint: string = buildUrl("repositories", organization, project, "pullrequests");
    const data: BitbucketMainResponse = await getCache(endpoint);
    const pullRequestIds = data.values.map((pr) => pr.id);
    await saveJSON(pullRequestIds, masterCacheFile);

    await Promise.all(
      pullRequestIds.map(async (id) => {
        const endpoint = buildUrl("repositories", organization, project, "pullrequests", id.toString());
        const data: any = await getCache(endpoint);
        
        const cacheFile = path.join(getCacheFolder(), `${id}.pr.json`);
        await saveJSON(data, cacheFile);
      })
    );


    return res.status(200).json({ success: true, message: "data" });
  } catch (error) {
    console.log(error);
    return res.status(500).json({ success: false, message: "Failed to fetch pull requests" });
  }
});

// Export the router
export default router;
