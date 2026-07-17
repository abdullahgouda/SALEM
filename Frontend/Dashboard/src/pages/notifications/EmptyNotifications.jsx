import emptyImg from "../../assets/nonotification.png";

function EmptyNotifications() {
    return (
        <div className="flex flex-col items-center justify-center mt-24 gap-4">
            <img src={emptyImg} className="w-64 opacity-90" />
            <h3 className="text-lg font-bold text-gray-700">
                لا توجد إشعارات حتى الآن
            </h3>
        </div>
    );
}

export default EmptyNotifications;
