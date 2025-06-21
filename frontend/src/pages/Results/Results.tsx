import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

function Results() {
    const navigate = useNavigate();
    const location = useLocation();
    const { score } = location.state || { score: 0 };

    const handleContinue = () => {
        navigate("/lessons");
    };

    return (
        <div className="flex flex-col h-screen w-full bg-beige-light p-8">
            <div className="flex-grow flex flex-col justify-center items-center text-center">
                <h1 className="text-2xl font-bold">Lesson Completed!</h1>
                
                <div className="my-8">
                    <p className="text-lg">Score</p>
                    <p className="text-6xl font-bold my-2">{Math.round(score)}%</p>
                    <p className="text-lg">Good Job!</p>
                </div>
            </div>
            
            <div className="flex justify-center">
                <Button className="w-full max-w-sm h-auto py-4" onClick={handleContinue}>
                    Continue
                </Button>
            </div>
        </div>
    );
}

export default Results; 