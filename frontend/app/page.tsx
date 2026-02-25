'use client';
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/upload', formData);
      setUploadResult(res.data);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadResult({ message: 'Error uploading file' });
    } finally {
      setLoading(false);
    }
  };

  const sendChat = async () => {
    if (!chatMessage.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:8000/chat', {
        message: chatMessage,
      });
      setChatResponse(res.data.reply);
    } catch (error) {
      console.error('Chat error:', error);
      setChatResponse('Sorry, something went wrong.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="text-center py-20">
        <h1 className="text-5xl font-bold mb-4">Your AI-Powered CA Assistant</h1>
        <p className="text-xl text-gray-300 mb-8">Upload documents, get instant insights, and chat with our intelligent advisor.</p>
        <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full text-lg transition">
          Try AI Assistant
        </button>
      </section>

      {/* AI Assistant Section */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-6">AI Assistant</h2>
        <div className="flex flex-col space-y-4">
          <div className="flex space-x-2">
            <input
              type="text"
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="Ask me anything about accounting, tax, etc."
              className="flex-1 px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-600 focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={sendChat}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg disabled:opacity-50"
            >
              Send
            </button>
          </div>
          {chatResponse && (
            <div className="bg-gray-800 p-4 rounded-lg">
              <p className="text-gray-200">{chatResponse}</p>
            </div>
          )}
        </div>
      </section>

      {/* Upload & Analysis Section */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-6">Accounting / Audit Solver</h2>
        <div className="border-2 border-dashed border-gray-500 rounded-lg p-8 text-center">
          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
          />
          <label htmlFor="file-upload" className="cursor-pointer">
            <div className="space-y-2">
              <p className="text-xl">Drag and drop or click to upload</p>
              <p className="text-sm text-gray-400">PDF, images (max 10MB)</p>
            </div>
          </label>
        </div>
        {loading && <p className="mt-4">Processing...</p>}
        {uploadResult && (
          <div className="mt-6 p-4 bg-gray-800 rounded-lg">
            <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(uploadResult, null, 2)}</pre>
          </div>
        )}
      </section>

      {/* About Us Section */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-4">About Us</h2>
        <p className="text-gray-300">We are a team of expert chartered accountants and AI specialists dedicated to making financial management easy and accessible.</p>
      </section>

      {/* Professional Experience */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-4">Professional Experience</h2>
        <ul className="list-disc list-inside text-gray-300 space-y-2">
          <li>20+ years in audit and assurance</li>
          <li>500+ successful client projects</li>
          <li>Specialized in tax planning for SMEs</li>
        </ul>
      </section>

      {/* CA Potential */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-4">CA Potential</h2>
        <p className="text-gray-300">Our AI model is trained on thousands of financial documents to provide accurate, real-time assistance.</p>
      </section>

      {/* Contact Us */}
      <section className="bg-white/10 backdrop-blur-lg rounded-2xl p-8">
        <h2 className="text-3xl font-semibold mb-4">Contact Us</h2>
        <form className="space-y-4">
          <input type="text" placeholder="Name" className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-600" />
          <input type="email" placeholder="Email" className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-600" />
          <textarea placeholder="Message" rows={4} className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-600"></textarea>
          <button className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg">Send</button>
        </form>
      </section>
    </div>
  );
}