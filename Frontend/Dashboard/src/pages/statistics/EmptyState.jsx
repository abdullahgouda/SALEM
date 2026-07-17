import noStatsImg from "../../assets/nostates.png";

function EmptyState() {
    return (
        <div className="flex flex-col items-center justify-center h-full text-center gap-7">
            <img src={noStatsImg} alt="No Statistics"
            className="w-80 opacity-90"/>

            <h3 className="text-lg font-bold text-gray-700">
                لا توجد إحصائيات حاليًا
            </h3>

          
        </div>
    );
}

export default EmptyState;
