import { useNavigate } from "react-router-dom";

import { X } from "lucide-react";
import { Progress } from "@/components/ui/progress";

function Study() {
    const navigate = useNavigate();

    const handleBack = () => {
        navigate("/lessons");
    }

    return (
        <div className="flex flex-col h-screen w-full bg-beige-light p-4 gap-4">
            <header className="flex justify-between items-center w-full">
                <X className="w-6 h-6" onClick={handleBack} />
                <Progress value={75} className="max-w-[300px]" />
            </header>
            <div className="flex flex-col items-center justify-center">
                <h1 className="text-2xl font-bold">Study</h1>
            </div>
        </div>
    )
}

export default Study;