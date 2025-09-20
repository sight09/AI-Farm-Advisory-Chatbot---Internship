const API_BASE_URL = "http://localhost:8000";

export interface ChatMessage {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  sources?: string[];
}

export interface ChatResponse {
  answer: string;
  sources: string[];
}

export interface ChatRequest {
  question: string;
  lang: string;
}

export const languages = [
  { code: "en", name: "English" },
  { code: "om", name: "Affan Oromo" },
  { code: "am", name: "Amharic" },
  { code: "ti", name: "Tigrigna" },
  { code: "so", name: "Somali" },
];

export async function sendMessage(
  question: string,
  lang: string
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, lang, location: "Dessie" }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error sending message:", error);
    throw new Error(
      "Failed to get response from the server. Please check if the backend is running at http://localhost:8000"
    );
  }
}

export async function uploadDocument(file: File): Promise<void> {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/embed`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
  } catch (error) {
    console.error("Error uploading document:", error);
    throw new Error("Failed to upload document");
  }
}
