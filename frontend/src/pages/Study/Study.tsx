import { useNavigate, useLocation, useParams, Navigate } from "react-router-dom";

import { X, Snail, Volume1, Bookmark, Mic } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import type { LessonBlockProps } from "@/components/LessonBlock/LessonBlock.types";

function Study() {
    const navigate = useNavigate();
    const location = useLocation();
    const { id } = useParams<{ id: string }>();
    const lesson = location.state?.lesson as LessonBlockProps | undefined;

    // Redirect if no lesson data or ID mismatch
    if (!lesson || lesson.id !== id) {
        return <Navigate to="/lessons" />;
    }

    const handleBack = () => {
        navigate("/lessons");
    }

    const handlePlay = () => {
        console.log("play", lesson.audio_url);
    }

    const handleSlowPlay = () => {
        console.log("slow play", lesson.audio_url);
    }

    const handleBookmark = () => {
        console.log("bookmark", lesson.id);
    }

    const handleSpeak = () => {
        console.log("speak", lesson.text);
    }

    return (
        <div className="flex flex-col h-screen w-full bg-beige-light">
            <div className="flex flex-col p-4 h-1/2">
                <div className="flex items-center">
                    <X className="w-8 h-8" onClick={handleBack} />
                    <Progress value={75} className="w-full ml-4"/>
                </div>
                <div className="flex flex-col w-full mt-4 h-full">
                    <p className="text-start text-[12px] font-[600] text-black-dark">Repeat After Me</p>
                    <div className="flex justify-center items-center h-full">
                        <div className="bg-gray-xlight w-[210px] h-[210px] rounded-full"/>                                            
                    </div>
                </div>                                
            </div>                        
            
            <div className="flex flex-col bg-white p-4 border rounded-t-2xl border-gray-light h-1/2">
                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <span className="bg-black-dark h-4 w-4 rounded-full mr-2" />
                        <p className="text-[12px] leading-6">Score</p>
                    </div>
                    <div className="flex items-center">                        
                        <p className="text-[16px] leading-6">98%</p>
                    </div>
                </div>    

                <p className="text-[32px] font-bold mt-4">{lesson.text}</p>
                <p className="text-[12px] font-bold mt-2">{lesson.translation}</p>
                
                <div className="flex items-center gap-4 mt-4">                    
                    <Volume1 className="text-primary size-7" onClick={handlePlay}/>
                    <Snail className="text-primary size-7" onClick={handleSlowPlay}/>                    
                    <Bookmark className="text-primary size-7" onClick={handleBookmark}/>                    
                </div>
                
                <div className="flex items-center justify-center h-full">
                    <Button className="w-[60px] h-[60px] rounded-full" onClick={handleSpeak}>
                        <Mic className="size-6" />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default Study;