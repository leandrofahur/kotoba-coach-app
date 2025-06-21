import { useNavigate } from "react-router-dom";

import { X, Snail, BookCheck, Book, Volume1, Bookmark, Mic } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";

function Study() {
    const navigate = useNavigate();

    const handleBack = () => {
        navigate("/lessons");
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
                <p className="text-[32px] font-bold mt-4">あの</p>
                <p className="text-[12px] font-bold mt-2">Translation</p>
                <div className="flex items-center gap-4 mt-4">
                    <Volume1 className="w-6 h-6" />
                    <Snail className="w-6 h-6" />
                    <Bookmark className="w-6 h-6" />
                </div>
                <div className="flex items-center justify-center h-full">
                    <Button className="w-[60px] h-[60px] rounded-full">
                        <Mic className="size-6" />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default Study;



// <div className="flex flex-col h-screen w-full bg-beige-light gap-4">
//     <div className="flex justify-between w-full p-4 h-1/2">
//         <X className="w-6 h-6" onClick={handleBack} />
//         <Progress value={75} className="max-w-[300px]" />                
//     </div>                        
//     {/* <div className="flex flex-col bg-white h-1/2 p-4">
//         <h1 className="text-2xl font-bold">Study</h1>                                    
//         <h1 className="text-2xl font-bold">Study</h1>
//         <h1 className="text-2xl font-bold">Study</h1>
//     </div> */}
// </div>