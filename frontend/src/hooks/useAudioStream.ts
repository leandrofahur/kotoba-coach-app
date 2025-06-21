import { useCallback, useRef } from 'react';

export const useAudioStream = (lessonId: string) => {
    const wsRef = useRef<WebSocket | null>(null);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);
    const feedbackReceivedRef = useRef(false);

    const startStreaming = useCallback(async () => {
        try {
            console.log('Starting audio stream...');
            feedbackReceivedRef.current = false;
            
            // Get microphone access
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    sampleRate: 16000,
                    channelCount: 1,
                    echoCancellation: true,
                    noiseSuppression: true
                }
            });

            console.log('Microphone access granted');

            // Create WebSocket connection
            wsRef.current = new WebSocket(`ws://localhost:8000/api/v1/audio-stream/ws/${lessonId}`);

            wsRef.current.onopen = () => {
                console.log('WebSocket connected');
            };

            wsRef.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('WebSocket received:', data);
                
                // Handle different types of feedback
                if (data.status === 'feedback') {
                    console.log(`Score: ${data.score}%`);
                    console.log(`Transcription: ${data.transcription}`);
                    console.log(`Expected: ${data.expected_text}`);
                    console.log(`Label: ${data.label}`);
                    
                    feedbackReceivedRef.current = true;
                    
                    // Emit custom event for UI updates
                    window.dispatchEvent(new CustomEvent('pronunciationFeedback', {
                        detail: data
                    }));
                    
                    // Now close the WebSocket after receiving feedback
                    setTimeout(() => {
                        if (wsRef.current?.readyState === WebSocket.OPEN) {
                            console.log('Feedback received, closing WebSocket');
                            wsRef.current.close();
                        }
                    }, 1000);
                } else if (data.status === 'chunk_received') {
                    console.log(`Chunk received: ${data.chunk_size} bytes, total: ${data.total_chunks}`);
                } else if (data.status === 'error') {
                    console.error('Processing error:', data.message);
                }
            };

            wsRef.current.onerror = (error) => {
                console.error('WebSocket error:', error);
            };

            wsRef.current.onclose = (event) => {
                console.log('WebSocket disconnected:', event.code, event.reason);
            };

            // Check available MIME types
            const mimeTypes = [
                'audio/webm;codecs=opus',
                'audio/webm',
                'audio/mp4',
                'audio/wav'
            ];
            
            const supportedType = mimeTypes.find(type => MediaRecorder.isTypeSupported(type));
            console.log('Supported MIME type:', supportedType);

            if (!supportedType) {
                throw new Error('No supported audio format found');
            }

            // Create MediaRecorder
            mediaRecorderRef.current = new MediaRecorder(stream, {
                mimeType: supportedType
            });

            console.log('MediaRecorder created with type:', supportedType);

            // Handle audio data
            mediaRecorderRef.current.ondataavailable = (event) => {
                console.log('Audio data available:', event.data.size, 'bytes');
                
                if (event.data.size > 0 && wsRef.current?.readyState === WebSocket.OPEN) {
                    // Convert to ArrayBuffer and send
                    event.data.arrayBuffer().then(buffer => {
                        console.log('Sending audio chunk:', buffer.byteLength, 'bytes');
                        wsRef.current?.send(buffer);
                    });
                } else {
                    console.log('Cannot send audio: WebSocket not ready or no data');
                }
            };

            // Start recording with smaller chunks for real-time processing
            mediaRecorderRef.current.start(100); // Send chunks every 100ms
            console.log('Started recording');

        } catch (error) {
            console.error('Error starting audio stream:', error);
            throw error;
        }
    }, [lessonId]);

    const stopStreaming = useCallback(() => {
        console.log('Stopping audio recording...');
        
        // Stop the MediaRecorder (stops sending audio data)
        if (mediaRecorderRef.current) {
            mediaRecorderRef.current.stop();
            console.log('MediaRecorder stopped - no more audio data will be sent');
        }
        
        // Send stop signal to backend (but keep WebSocket open)
        if (wsRef.current?.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify({ action: 'stop' }));
            console.log('Sent stop signal to backend - waiting for feedback');
        }
        
        // Don't close the WebSocket here - let it stay open for feedback
        // The WebSocket will be closed automatically when feedback is received
    }, []);

    return { startStreaming, stopStreaming };
}; 