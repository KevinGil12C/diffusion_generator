<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Contracts\HttpClient\HttpClientInterface;

final class GeneratorController extends AbstractController
{
    public function __construct(
        private HttpClientInterface $httpClient,
        private \Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface $params
    ) {}

    #[Route('/api/gallery', name: 'api_gallery', methods: ['GET'])]
    public function gallery(): JsonResponse
    {
        $outputsDir = $this->params->get('kernel.project_dir') . '/public/outputs';
        $files = glob($outputsDir . '/*.{png,mp4}', GLOB_BRACE);
        
        $images = [];
        foreach ($files as $file) {
            $images[] = [
                'filename' => basename($file),
                'url' => 'outputs/' . basename($file),
                'time' => filemtime($file),
                'type' => str_ends_with($file, '.mp4') ? 'video' : 'image'
            ];
        }
        
        // Sort by newest first
        usort($images, fn($a, $b) => $b['time'] - $a['time']);

        return new JsonResponse($images);
    }

    #[Route('/api/delete-file', name: 'api_delete_file', methods: ['POST'])]
    public function deleteFile(Request $request): JsonResponse
    {
        $content = $request->getContent();
        $data = json_decode($content, true);
        $filename = $data['filename'] ?? null;

        if (!$filename) {
            return new JsonResponse(['status' => 'error', 'message' => 'Filename required'], 400);
        }

        // Basic sanity check to prevent directory traversal
        if (str_contains($filename, '/') || str_contains($filename, '\\')) {
            return new JsonResponse(['status' => 'error', 'message' => 'Invalid filename'], 400);
        }

        $filePath = $this->params->get('kernel.project_dir') . '/public/outputs/' . basename($filename);
        
        if (file_exists($filePath)) {
            unlink($filePath);
            return new JsonResponse(['status' => 'success']);
        }
        
        return new JsonResponse(['status' => 'error', 'message' => 'File not found', 'checked_path' => $filePath], 404);
    }

    #[Route('/api/server/status', name: 'api_server_status', methods: ['GET'])]
    public function serverStatus(): JsonResponse
    {
        try {
            $response = $this->httpClient->request('GET', 'http://127.0.0.1:8000/', ['timeout' => 2]);
            return new JsonResponse(['status' => 'online', 'code' => $response->getStatusCode()]);
        } catch (\Exception $e) {
            return new JsonResponse(['status' => 'offline']);
        }
    }

    #[Route('/api/server/restart', name: 'api_server_restart', methods: ['POST'])]
    public function restartServer(): JsonResponse
    {
        // Use absolute path for safety in XAMPP
        $batFile = 'C:\xampp\htdocs\diffusion_generator\api\start_backend.bat';
        
        if (file_exists($batFile)) {
            // Run visibly so user can see the terminal
            pclose(popen("start cmd /c \"$batFile\"", "r"));
            return new JsonResponse(['status' => 'success', 'message' => 'Restart signal sent']);
        }
        
        return new JsonResponse(['status' => 'error', 'message' => 'Script not found'], 500);
    }

    #[Route('/', name: 'app_generator')]
    public function index(): Response
    {
        return $this->render('generator/index.html.twig');
    }

    #[Route('/api/generate', name: 'api_generate', methods: ['POST'])]
    public function generate(Request $request): JsonResponse
    {
        set_time_limit(3600);
        $content = $request->getContent();
        $data = json_decode($content, true);
        
        if (json_last_error() !== JSON_ERROR_NONE || !is_array($data)) {
            return new JsonResponse(['status' => 'error', 'message' => 'Invalid JSON payload'], 400);
        }

        $prompt = $data['prompt'] ?? '';
        
        // --- AI MAGIC: Translate Human Language to PROMPT ---
        if ($data['magic'] ?? false) {
            try {
                $systemPrompt = "You are a Stable Diffusion Prompt Engineer. Translate the user's request into a highly detailed comma-separated prompt. If they ask to 'improve' or 'modify' an existing idea, combine the old idea with new details. Include lighting, style, and artistic technical terms. ONLY return the prompt tags.";
                $magicResponse = $this->httpClient->request('GET', 'https://text.pollinations.ai/' . urlencode($prompt), [
                    'timeout' => 8,
                    'query' => [
                        'model' => 'openai',
                        'system' => $systemPrompt
                    ]
                ]);
                
                if ($magicResponse->getStatusCode() === 200) {
                    $prompt = trim($magicResponse->getContent(false));
                }
            } catch (\Exception $e) {
                // Fallback to original prompt on failure
            }
        }

        try {
            $response = $this->httpClient->request('POST', 'http://127.0.0.1:8000/generate', [
                'timeout' => 3600,
                'json' => [
                    'mode' => $data['mode'] ?? 'txt2img',
                    'prompt' => $prompt,
                    'negative_prompt' => $data['negative_prompt'] ?? '',
                    'model_name' => $data['model'] ?? 'v1-5-pruned-emaonly.safetensors',
                    'steps' => (int)($data['steps'] ?? 20),
                    'cfg' => (float)($data['cfg'] ?? 7.0),
                    'strength' => (float)($data['strength'] ?? 0.75),
                    'init_image' => $data['init_image'] ?? null,
                    'seed' => (int)($data['seed'] ?? -1),
                ]
            ]);

            $result = $response->toArray();
            $result['expanded_prompt'] = $prompt;

            return new JsonResponse($result);
        } catch (\Exception $e) {
            return new JsonResponse(['status' => 'error', 'message' => $e->getMessage()], 500);
        }
    }
}
