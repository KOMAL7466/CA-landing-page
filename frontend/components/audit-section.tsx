'use client'

import { useState } from 'react'
import axios from 'axios'
import { Upload, FileText, X, CheckCircle, AlertCircle, Loader2, FileSearch } from 'lucide-react'
import { motion } from 'framer-motion'

// ✅ Correct BASE_URL - your live backend
const BASE_URL = 'https://ca-landing-page.onrender.com'

export default function AuditSection() {
  const [file, setFile] = useState<File | null>(null)
  const [query, setQuery] = useState('Perform audit on this financial document and highlight key points.')
  const [year, setYear] = useState('2025-2026')
  const [loading, setLoading] = useState(false)
  const [auditResult, setAuditResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setError(null)
    }
  }

  const clearFile = () => {
    setFile(null)
    setAuditResult(null)
  }

  const runAudit = async () => {
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)
    formData.append('query', query)
    formData.append('year', year)

    try {
      // ✅ Correct endpoint: /api/audit
      const res = await axios.post(`${BASE_URL}/api/audit`, formData)

      if (res.data.status === 'success') {
        setAuditResult(res.data)
      } else {
        setError(res.data.message || 'Audit failed')
      }
    } catch (err) {
      console.error('Audit error:', err)
      setError('Failed to run audit. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section id="audit-section" className="py-24 px-4 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            AI Audit Assistant
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Upload your financial documents and get a detailed AI-powered audit
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left - Upload Form */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
          >
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
              <FileSearch className="w-6 h-6 text-blue-600" />
              Upload for Audit
            </h3>

            {/* File Upload Area */}
            {!file ? (
              <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-xl p-8 text-center hover:border-blue-500 transition cursor-pointer mb-6">
                <input
                  type="file"
                  id="audit-file-upload"
                  className="hidden"
                  accept=".pdf,.jpg,.jpeg,.png,.xlsx,.xls,.csv"
                  onChange={handleFileUpload}
                />
                <label htmlFor="audit-file-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                  <p className="text-gray-600 dark:text-gray-300 font-medium mb-2">
                    Click to upload financial document
                  </p>
                  <p className="text-sm text-gray-400">
                    PDF, Excel, Images (Max 10MB)
                  </p>
                </label>
              </div>
            ) : (
              <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-4 mb-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <FileText className="w-8 h-8 text-blue-600" />
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white truncate max-w-50">
                        {file.name}
                      </p>
                      <p className="text-xs text-gray-400">
                        {(file.size / 1024).toFixed(2)} KB
                      </p>
                    </div>
                  </div>
                  <button
                    onClick={clearFile}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
            )}

            {/* Financial Year */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Financial Year
              </label>
              <input
                type="text"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                className="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900"
                placeholder="e.g., 2025-2026"
              />
            </div>

            {/* Query */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Audit Query (Optional)
              </label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={3}
                className="w-full px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-900"
                placeholder="Add specific audit instructions..."
              />
            </div>

            {/* Run Audit Button */}
            <button
              onClick={runAudit}
              disabled={!file || loading}
              className="w-full px-6 py-3 bg-linear-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg disabled:opacity-50 transition font-medium flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Running Audit...
                </>
              ) : (
                <>
                  <FileSearch className="w-4 h-4" />
                  Run AI Audit
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg flex items-center gap-2 text-red-600 dark:text-red-400">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm">{error}</span>
              </div>
            )}
          </motion.div>

          {/* Right - Audit Results */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6"
          >
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              Audit Report
            </h3>

            {!auditResult ? (
              <div className="h-96 flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <FileSearch className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p className="text-lg">No audit run yet</p>
                  <p className="text-sm mt-2">Upload a document and click "Run AI Audit"</p>
                </div>
              </div>
            ) : (
              <div className="h-96 overflow-y-auto pr-2">
                {/* Confidence Score Badge */}
                {auditResult.structured_data?.risk_score && (
                  <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        Audit Confidence:
                      </span>
                      <span className={`text-lg font-bold ${
                        auditResult.structured_data.risk_score > 80 
                          ? 'text-green-600' 
                          : auditResult.structured_data.risk_score > 50
                          ? 'text-yellow-600'
                          : 'text-red-600'
                      }`}>
                        {auditResult.structured_data.risk_score}%
                      </span>
                    </div>
                  </div>
                )}

                {/* Audit Report Text */}
                <div className="prose prose-sm dark:prose-invert max-w-none">
                  {auditResult.audit_report?.split('\n').map((line: string, i: number) => {
                    if (line.startsWith('#')) {
                      const text = line.replace(/^#+\s*/, '')
                      return <h3 key={i} className="font-bold text-lg mt-4 mb-2">{text}</h3>
                    } else if (line.startsWith('-') || line.startsWith('*')) {
                      return <li key={i} className="ml-4 mb-1 text-gray-700 dark:text-gray-300">{line.substring(1).trim()}</li>
                    } else if (line.trim() === '') {
                      return <br key={i} />
                    } else {
                      return <p key={i} className="mb-2 text-gray-700 dark:text-gray-300">{line}</p>
                    }
                  })}
                </div>

                <div className="mt-4 text-xs text-gray-400">
                  Audited on: {new Date(auditResult.audit_date).toLocaleString()}
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </section>
  )
}