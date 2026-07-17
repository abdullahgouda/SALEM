import noWorkImg from "../../assets/noworkflow.png";

function EmptyWork() {
    return (
        <div className="flex flex-col items-center justify-center h-full text-center gap-7">
            <img src={noWorkImg} alt="No Workflow"className="w-80 opacity-90"/>

            <h3 className="text-lg font-bold text-gray-700">
               لا توجدأعمال حالية حتي الأن
            </h3>

            <p className="text-sm text-gray-500 max-w-sm">
                عند وصول أعمال جديدة ستظهر هنا تلقائيًا
            </p>
        </div>
    );
}

export default EmptyWork;
