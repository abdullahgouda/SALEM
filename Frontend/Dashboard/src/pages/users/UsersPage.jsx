import { useState, useEffect } from "react";

import UsersFilters from "./UsersFilters";
import UsersCards from "./UsersCards";
import UsersTableHeader from "./UsersTableHeader";
import UsersTableRows from "./UsersTableRows";
import AddUserModal from "./AddUserPage";
import EditUserModal from "./EditUserModal";
import { useTranslation } from "react-i18next";

import {
    getUsers,
    deleteUser,
    updateUser,
    createUser,
} from "../../api/users_api";

function UsersPage() {

    const { t } = useTranslation();

    /* ===== USERS STATE ===== */
    const [users, setUsers] = useState([]);

    /* ===== LOADING ===== */
    const [loading, setLoading] = useState(true);

    /* ===== FILTERS ===== */
    const [role, setRole] = useState("");
    const [search, setSearch] = useState("");

    /* ===== MODALS ===== */
    const [openAdd, setOpenAdd] = useState(false);
    const [openEdit, setOpenEdit] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);

    /* ===== PAGINATION ===== */
    const [page, setPage] = useState(1);
    const perPage = 12;

    /* ================= FETCH USERS ================= */
    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            setLoading(true);

            const data = await getUsers();

            setUsers(data);

        } catch (err) {
            console.error("Users fetch error", err);
            setUsers([]);
        } finally {
            setLoading(false);
        }
    };

    /* ===== FILTER ===== */
    const filteredUsers = users.filter((u) => {

        const matchSearch =
            u.name?.toLowerCase().includes(search.toLowerCase()) ||
            u.email?.toLowerCase().includes(search.toLowerCase());

        const matchRole =
            !role || u.role === role;

        return matchSearch && matchRole;
    });

    const startIndex = (page - 1) * perPage;

    const visibleUsers = filteredUsers.slice(
        startIndex,
        startIndex + perPage
    );

    const totalPages = Math.max(
        1,
        Math.ceil(filteredUsers.length / perPage)
    );

    /* ===== TABLE VIEW ===== */
    const isTableView = role !== "" || search !== "";

    /* ================= DELETE USER ================= */
    const handleDeleteUser = async (id) => {
        try {

            await deleteUser(id);

            await fetchUsers();

        } catch (err) {
            console.error(err);
        }
    };

    /* ================= EDIT USER ================= */
    const handleSaveEdit = async (updatedUser) => {
        try {

            await updateUser(updatedUser.id, updatedUser);

            await fetchUsers();

            setOpenEdit(false);

        } catch (err) {
            console.error(err);
        }
    };

    /* ================= ADD USER ================= */
    const handleAddUser = async (newUser) => {
        try {

            await createUser(newUser);

            await fetchUsers();

            setOpenAdd(false);

        } catch (err) {
            console.error(err);
        }
    };

    return (
        <div className="p-4 flex flex-col h-full">

            {/* ===== FILTERS ===== */}
            <UsersFilters
                onAddUser={() => setOpenAdd(true)}
                onSearchChange={setSearch}
                onRoleChange={setRole}
            />

            {/* ===== CONTENT ===== */}
            <div className="flex-1">

                {loading ? (
                    <p className="text-center py-10 text-gray-500">
                        {t("loading")}
                    </p>
                ) : (
                    <>
                        {/* ===== CARDS ===== */}
                        {!isTableView && (
                            <>
                                <UsersCards
                                    users={visibleUsers}
                                    onEdit={(user) => {
                                        setSelectedUser(user);
                                        setOpenEdit(true);
                                    }}
                                />
                            </>
                        )}

                        {/* ===== TABLE ===== */}
                        {isTableView && (
                            <div className="overflow-x-auto">
                                <UsersTableHeader />

                                <UsersTableRows
                                    users={visibleUsers}
                                    onEdit={(user) => {
                                        setSelectedUser(user);
                                        setOpenEdit(true);
                                    }}
                                    onDelete={handleDeleteUser}
                                />
                            </div>
                        )}
                    </>
                )}
            </div>

            {/* ===== PAGINATION ===== */}
            <div className="flex justify-between items-center mt-4 text-sm">
                <span className="text-gray-500">
                    {t("page")} {page} {t("of")} {totalPages}
                </span>

                <div className="flex gap-2">
                    <button
                        disabled={page === 1}
                        onClick={() => setPage((p) => Math.max(p - 1, 1))}
                        className="px-3 py-1 rounded-lg border disabled:opacity-40">
                        {t("previous")}
                    </button>

                    <button
                        disabled={page === totalPages}
                        onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
                        className="px-3 py-1 rounded-lg border disabled:opacity-40">
                        {t("next")}
                    </button>
                </div>
            </div>

            {/* ===== EDIT MODAL ===== */}
            {openEdit && (
                <EditUserModal
                    user={selectedUser}
                    onClose={() => setOpenEdit(false)}
                    onSave={handleSaveEdit}
                />
            )}

            {/* ===== ADD MODAL ===== */}
            {openAdd && (
                <AddUserModal
                    onClose={() => setOpenAdd(false)}
                    onAdd={handleAddUser}
                />
            )}
        </div>
    );
}

export default UsersPage;