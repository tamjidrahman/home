"use client"

import { useEffect, useRef, useState } from "react"
import { Settings } from "lucide-react"
import { getToken, setToken, clearToken } from "@/lib/auth"

type Props = { onChange?: () => void }

export function TokenSettings({ onChange }: Props) {
  const [open, setOpen] = useState(false)
  const [hasToken, setHasToken] = useState(false)
  const [input, setInput] = useState("")
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    setHasToken(!!getToken())
  }, [])

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false)
    }
    window.addEventListener("keydown", onKey)
    inputRef.current?.focus()
    return () => window.removeEventListener("keydown", onKey)
  }, [open])

  const save = () => {
    if (!input.trim()) return
    setToken(input.trim())
    setHasToken(true)
    setInput("")
    setOpen(false)
    onChange?.()
  }

  const clear = () => {
    clearToken()
    setHasToken(false)
    onChange?.()
  }

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        aria-label="Settings"
        className="rounded p-2 text-muted-foreground hover:bg-muted hover:text-foreground"
      >
        <Settings className="h-5 w-5" />
      </button>

      {open && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
          onClick={() => setOpen(false)}
        >
          <div
            className="w-full max-w-md rounded-lg border border-border bg-background p-6 shadow-lg"
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="mb-4 text-lg font-semibold">Settings</h2>

            <div className="mb-2 flex items-center justify-between">
              <label htmlFor="ha-token" className="text-sm font-medium">
                Home Assistant token
              </label>
              {hasToken && (
                <span className="text-xs text-muted-foreground">currently set</span>
              )}
            </div>

            <input
              id="ha-token"
              ref={inputRef}
              type="password"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && save()}
              placeholder={hasToken ? "Enter a new token to replace" : "Bearer token"}
              className="mb-4 w-full rounded border border-input bg-background px-3 py-2 text-sm"
            />

            <div className="flex justify-between">
              {hasToken ? (
                <button
                  onClick={clear}
                  className="rounded px-3 py-2 text-sm text-destructive hover:bg-muted"
                >
                  Clear token
                </button>
              ) : (
                <span />
              )}
              <div className="flex gap-2">
                <button
                  onClick={() => setOpen(false)}
                  className="rounded px-3 py-2 text-sm text-muted-foreground hover:bg-muted"
                >
                  Cancel
                </button>
                <button
                  onClick={save}
                  disabled={!input.trim()}
                  className="rounded bg-primary px-3 py-2 text-sm text-primary-foreground disabled:opacity-50"
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
