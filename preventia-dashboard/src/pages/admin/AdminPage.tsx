import React from 'react';
import { AdminLayout } from './AdminLayout';
import { SourcesAdminPage } from './SourcesAdminPage';

export const AdminPage: React.FC = () => {
  return (
    <AdminLayout>
      <SourcesAdminPage />
    </AdminLayout>
  );
};
