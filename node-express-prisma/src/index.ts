import express, { Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import { z } from 'zod';
import dotenv from 'dotenv';
dotenv.config();
const app = express();
const prisma = new PrismaClient();
const PORT = process.env.PORT || 3000;
app.use(express.json());
// 1. Schemi di Validazione Input con Zod
const CreateUserSchema = z.object({
  email: z.string().email("Formato email non valido"),
  name: z.string().min(2, "Il nome deve avere almeno 2 caratteri"),
});
const CreatePostSchema = z.object({
  title: z.string().min(1, "Il titolo è obbligatorio"),
  content: z.string().min(1, "Il contenuto è obbligatorio"),
  authorId: z.number().int().positive(),
  views: z.number().int().nonnegative().optional(),
});
const UpdatePostSchema = z.object({
  title: z.string().min(1).optional(),
  content: z.string().min(1).optional(),
  views: z.number().int().nonnegative().optional(),
});
// 2. Rotte CRUD: USERS
app.post('/users', async (req: Request, res: Response) => {
  try {
    const data = CreateUserSchema.parse(req.body);
    const user = await prisma.user.create({ data });
    res.status(201).json(user);
  } catch (err: any) {
    res.status(400).json({ error: err.errors || err.message });
  }
});
app.get('/users', async (_req: Request, res: Response) => {
  const users = await prisma.user.findMany({ include: { posts: true } });
  res.json(users);
});
// 3. Rotte CRUD: POSTS
app.post('/posts', async (req: Request, res: Response) => {
  try {
    const data = CreatePostSchema.parse(req.body);
    const post = await prisma.post.create({ data });
    res.status(201).json(post);
  } catch (err: any) {
    res.status(400).json({ error: err.errors || err.message });
  }
});
app.put('/posts/:id', async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    const data = UpdatePostSchema.parse(req.body);
    const updated = await prisma.post.update({ where: { id }, data });
    res.json(updated);
  } catch (err: any) {
    res.status(400).json({ error: err.errors || "Post non trovato o dati errati" });
  }
});
app.delete('/posts/:id', async (req: Request, res: Response) => {
  try {
    const id = Number(req.params.id);
    await prisma.post.delete({ where: { id } });
    res.status(204).send();
  } catch {
    res.status(404).json({ error: "Post non trovato" });
  }
});
// 4. Query Complessa: JOIN + GROUP BY + ORDER BY
app.get('/analytics/users-summary', async (_req: Request, res: Response) => {
  const usersWithStats = await prisma.user.findMany({
    select: {
      id: true,
      name: true,
      posts: { select: { views: true } },
    },
  });
  const summary = usersWithStats
    .map((u) => ({
      userId: u.id,
      userName: u.name,
      totalPosts: u.posts.length,
      totalViews: u.posts.reduce((acc, p) => acc + p.views, 0),
    }))
    .sort((a, b) => b.totalViews - a.totalViews);
  res.json(summary);
});
app.listen(PORT, () => {
  console.log(`Server Node.js attivo su http://localhost:${PORT}`);
});