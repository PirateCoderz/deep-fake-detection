# Frontend Setup Guide

Quick guide to get the Next.js frontend running.

## Prerequisites

- Node.js 18+ installed
- npm or yarn
- Backend API running on `http://localhost:8000`

## Installation Steps

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

This will install:
- Next.js 14
- React 18
- TypeScript
- Material-UI
- Axios
- React Dropzone
- And all other dependencies

### 3. Create Environment File
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Fake Product Detection
NEXT_PUBLIC_MAX_FILE_SIZE_MB=10
```

### 4. Start Development Server
```bash
npm run dev
```

The app will be available at: **http://localhost:3000**

## Verify Installation

1. Open http://localhost:3000
2. You should see the upload page
3. Try uploading an image (backend must be running)

## Common Issues

### Port 3000 Already in Use
```bash
# Use different port
PORT=3001 npm run dev
```

### Module Not Found Errors
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### API Connection Errors
- Ensure backend is running on port 8000
- Check CORS settings in backend
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`

## Development Commands

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Run linter
npm run lint

# Run tests (when implemented)
npm test
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js pages (server components)
│   ├── components/       # React components (client components)
│   ├── hooks/            # Custom React hooks
│   ├── services/         # API services
│   ├── types/            # TypeScript types
│   ├── utils/            # Utility functions
│   └── data/             # Mock data
├── public/               # Static files
└── package.json          # Dependencies
```

## Features

- ✅ Drag & drop image upload
- ✅ Real-time classification
- ✅ Results visualization
- ✅ User feedback form
- ✅ Error handling
- ✅ Responsive design

## Next Steps

1. Start backend: `python backend/src/main.py`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
4. Upload an image to test

## Production Deployment

### Build
```bash
npm run build
```

### Start
```bash
npm start
```

### Environment Variables for Production
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## Support

- Frontend README: `frontend/README.md`
- Task 12 Summary: `12_FRONTEND_COMPLETE.md`
- Backend API Docs: http://localhost:8000/docs

---

**Ready to use!** 🚀
