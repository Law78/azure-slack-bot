import { app } from '@azure/functions';
import { handler } from './handler';

app.http('slack', {
  methods: ['GET'],
  authLevel: 'anonymous',
  route: 'v1/slack', //api/v1/slack
  handler
})