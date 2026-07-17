function UsersCards({ users, onEdit }) {
    return (
        <div
            className="
                grid
                grid-cols-1
                sm:grid-cols-2
                lg:grid-cols-3
                xl:grid-cols-4
                gap-4
            "
        >
            {users.map((user) => (
                <div
                    key={user.id}
                    onClick={() => onEdit(user)}
                    className="
                        bg-white rounded-xl shadow p-4 text-center
                        cursor-pointer hover:shadow-lg transition
                    "
                >
                    <img
                        src={
                            user.image ||
                            `https://i.pravatar.cc/150?img=${user.id + 20}`
                        }
                        className="w-12 h-12 rounded-full mx-auto mb-2"
                        alt="avatar"
                    />

                    <h4 className="text-sm font-semibold truncate">
                        {user.name}
                    </h4>

                    <p className="text-xs text-gray-500 truncate">
                        {user.role}
                    </p>

                    <p className="text-[11px] text-gray-400 truncate">
                        {user.email}
                    </p>
                </div>
            ))}
        </div>
    );
}

export default UsersCards;