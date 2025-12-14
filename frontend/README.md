# Fake Product Detection - Frontend

Next.js frontend application for the Fake Product Detection system.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **UI Library**: Material-UI (MUI)
- **Styling**: Tailwind CSS + Emotion (MUI)
- **HTTP Client**: Axios
- **File Upload**: React Dropzone
- **Testing**: Jest + React Testing Library

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout (server component)
│   │   ├── page.tsx            # Home page (server component)
│   │   ├── results/[id]/       # Results page route
│   │   └── globals.css         # Global styles
│   ├── components/             # React components
│   │   ├── pages/              # Page-level components (client)
│   │   │   ├── HomePage.tsx
│   │   │   └── ResultsPage.tsx
│   │   ├── upload/             # Upload-related components
│   │   │   ├── ImageUploader.tsx
│   │   │   └── ImagePreview.tsx
│   │   ├── results/            # Results-related components
│   │   │   ├── ClassificationBadge.tsx
│   │   │   ├── ConfidenceScore.tsx
│   │   │   ├── ExplanationsList.tsx
│   │   │   └── FeedbackForm.tsx
│   │   └── providers/          # Context providers
│   │       └── ThemeProvider.tsx
│   ├── hooks/                  # Custom React hooks
│   │   ├── useClassification.ts
│   │   └── useFeedback.ts
│   ├── services/               # API services
│   │   └── api.ts
│   ├── types/                  # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/                  # Utility functions
│   │   └── validation.ts
│   └── data/                   # Mock/dummy data
│       └── mockData.ts
├── public/                     # Static assets
├── next.config.js              # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies

```

## Architecture

### Server vs Client Components

- **Server Components** (`page.tsx`, `layout.tsx`):
  - Handle routing and metadata
  - No client-side JavaScript
  - Better SEO and performance

- **Client Components** (components with `'use client'`):
  - Interactive UI elements
  - State management
  - Event handlers
  - API calls

### Data Flow

1. User uploads image on HomePage
2. Image sent to backend API via `useClassification` hook
3. Result stored in sessionStorage
4. Navigate to ResultsPage with request ID
5. ResultsPage displays results and feedback form

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation

```bash
cd frontend
npm install
```

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Fake Product Detection
NEXT_PUBLIC_MAX_FILE_SIZE_MB=10
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Build

```bash
npm run build
npm start
```

### Testing

```bash
npm test
npm run test:watch
```

## Features

### Image Upload
- Drag & drop interface
- File validation (type, size)
- Image preview
- Support for JPEG, PNG, HEIC

### Classification
- Real-time processing indicator
- Confidence score visualization
- Classification badge (Original/Fake)
- Detailed explanations

### Results Display
- Circular progress indicator
- Color-coded confidence levels
- Heatmap support (when available)
- Processing time display

### User Feedback
- Correct/Incorrect buttons
- Optional comments
- Success confirmation

### Error Handling
- File validation errors
- API error messages
- Network error handling
- User-friendly error messages

## API Integration

### Endpoints Used

- `POST /api/v1/classify` - Upload and classify image
- `POST /api/v1/feedback` - Submit user feedback
- `GET /api/v1/health` - Check API health
- `GET /api/v1/stats` - Get system statistics

### API Service

Located in `src/services/api.ts`:

```typescript
import { api } from '@/services/api';

// Classify image
const result = await api.classifyImage(file);

// Submit feedback
await api.submitFeedback({
  request_id: 'xxx',
  is_correct: true,
});
```

## Custom Hooks

### useClassification

```typescript
const { classify, loading, error, result } = useClassification();

await classify(file);
```

### useFeedback

```typescript
const { submitFeedback, loading, error, success } = useFeedback();

await submitFeedback({ request_id, is_correct: true });
```

## Components

### ImageUploader
- Drag & drop file upload
- File validation
- Preview generation

### ClassificationBadge
- Visual classification result
- Color-coded (green/red)
- Confidence display

### ConfidenceScore
- Circular progress indicator
- Percentage display
- Color-coded by confidence level

### ExplanationsList
- Detailed analysis reasons
- Icon-based list
- Expandable items

### FeedbackForm
- Correct/Incorrect buttons
- Comments field
- Success/error handling

## Styling

### Material-UI Theme

Customized theme in `ThemeProvider.tsx`:
- Primary: Blue (#1976d2)
- Secondary: Pink (#dc004e)
- Success: Green (#4caf50)
- Error: Red (#f44336)
- Warning: Orange (#ff9800)

### Tailwind CSS

Used for utility classes and layout helpers.

## Performance Optimizations

- Next.js Image component for optimized images
- Server-side rendering for initial page load
- Client-side navigation with Next.js router
- SessionStorage for result caching
- Lazy loading of components

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

### Vercel (Recommended)

```bash
npm run build
# Deploy to Vercel
```

### Docker

```bash
docker build -t fake-detection-frontend .
docker run -p 3000:3000 fake-detection-frontend
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## Troubleshooting

### API Connection Issues

- Check backend is running on port 8000
- Verify CORS settings in backend
- Check network tab in browser DevTools

### Image Upload Fails

- Check file size (<10MB)
- Verify file format (JPEG, PNG, HEIC)
- Check backend logs for errors

### Build Errors

```bash
rm -rf .next node_modules
npm install
npm run build
```

## Future Enhancements

- [ ] Real-time heatmap visualization
- [ ] Batch image upload
- [ ] Classification history
- [ ] User authentication
- [ ] Dark mode toggle
- [ ] Mobile camera capture
- [ ] Progressive Web App (PWA)
- [ ] Internationalization (i18n)

## Contributing

1. Follow TypeScript strict mode
2. Use functional components with hooks
3. Keep components small and focused
4. Write tests for new features
5. Follow Material-UI design guidelines

## License

MIT
