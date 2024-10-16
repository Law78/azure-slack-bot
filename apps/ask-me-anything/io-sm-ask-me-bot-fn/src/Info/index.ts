import { app } from '@azure/functions';
import { handler } from './handler';

app.http('info', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'v1/info',
  handler
})