import editIcon from "../../assets/icons/edit.png";
import deleteIcon from "../../assets/trash.png";

function UsersTableRows({ users, onDelete, onEdit }) {

    return (
        <div className="min-w-[900px] bg-white rounded-xl shadow mt-2 divide-y">
            {users.map((user) => (
                <div
                    key={user.id}
                    className="
                        grid grid-cols-6
                        items-center
                        text-center
                        px-4 py-3
                        text-sm
                    "
                >
                    <div className="font-medium truncate">
                        {user.name}
                    </div>

                    <div className="truncate text-gray-600">
                        {user.email}
                    </div>

                    <div>{user.role}</div>

                    {/* STATUS */}
                    <div
                        className={
                            user.status === "نشط"
                                ? "text-green-600 font-semibold"
                                : "text-red-500 font-semibold"
                        }
                    >
                        {user.status}
                    </div>

                    <div className="text-gray-500 text-xs leading-tight">
                        <div>{user.lastLoginDate}</div>
                        <div>{user.lastLoginTime}</div>
                    </div>

                    <div className="flex justify-center gap-3">
                        <img
                            src={editIcon}
                            className="w-4 h-4 cursor-pointer"
                            onClick={() => onEdit(user)}
                        />

                        <img
                            src={deleteIcon}
                            className="w-4 h-4 cursor-pointer"
                            onClick={() => onDelete(user.id)}
                        />
                    </div>
                </div>
            ))}
        </div>
    );
}

export default UsersTableRows;