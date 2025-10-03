# 🧪 Weblet — Minimal Semantic Protocol Toy

This is a **tiny, local-only experiment** exploring an alternative way for devices to talk to each other — not through URLs and web pages, but through **semantic queries**: asking by *meaning* instead of *location*.

> ⚠️ **Disclaimer:** This is a **playful prototype**, not a real internet replacement. There is no security, no mesh, no guarantees. It’s just a small step toward imagining different networking ideas.

---

## ✨ What It Does

* Runs a simple TCP server and client on your machine.
* Client sends a **JSON query** describing *what it wants* (e.g., a quote with a certain mood).
* Server looks up the best match in a **tiny in-memory object store** and responds.
* Uses newline-delimited JSON messages, not HTTP.

That’s all — no DNS, no HTML, no browsers.

---

## 🚀 Quick Start

### 1. Run the Server

```bash
python weblet.py server 127.0.0.1 8088
```

### 2. Run the Client

```bash
python weblet.py client 127.0.0.1 8088 '{"type":"quote","mood":"motivational"}'
```

You should see a **HELLO** message from the server, followed by a matching object.

---

## 🧠 Why This Exists

The goal is **not** to replace the web, but to experiment with:

* Semantic addressing (querying by intent)
* Stateful message flows without HTTP
* Thinking from first principles

This is a stepping stone for bigger ideas — like building richer local networks — but this repo keeps it deliberately minimal and understandable.

---

## 📝 Next Steps (Optional)

If you want to tinker:

* Add more objects to the store.
* Change the query resolution logic.
* Extend the message types (e.g., add `STATE` or negotiation).

---

## ⚠️ Limitations

* Not secure. Don’t expose it to the public internet.
* Single server, single client. No mesh, no discovery.
* Designed for clarity, not performance.

---

## 📄 License

MIT — free to use, modify, and share, but **no warranty**.
