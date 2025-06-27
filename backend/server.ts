// Import .env variables
import dotenv from "dotenv";

// Import Node Modules
import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from 'url';

// Server Variables
dotenv.config();
const app = express();
const PORT: number = Number(process.env.PORT) || 80;
const HOST: string = process.env.HOST || "0.0.0.0";
process.env.ROOT_DIR = path.dirname(__dirname)

// CORS
app.use(cors());

// Json Parsing
app.use(express.json());

// Middleware
import BitBucketHandler from "./routes/bitbucket";

// Use Routes
app.use("/API", BitBucketHandler);


// Start the server
app.listen(PORT, HOST, (err?: any) => {
  if (err) {
    console.error("Server failed:", err);
    process.exit(1);
  }
  console.log(`Server is running on http://${HOST}:${PORT}`);
});


