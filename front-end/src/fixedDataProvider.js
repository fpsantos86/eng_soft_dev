import { fetchUtils } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

const apiUrl = 'http://localhost:7000/api'; // URL base da API
const httpClient = fetchUtils.fetchJson;

const customDataProvider = simpleRestProvider(apiUrl, httpClient);

const fixedDataProvider = {
    ...customDataProvider,
    getList: (resource, params) => {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;
        const query = {
            filter: JSON.stringify(params.filter),
            range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
            sort: JSON.stringify([field, order]),
        };
        const url = `${apiUrl}/${resource}/?${new URLSearchParams(query).toString()}`;
        return httpClient(url).then(({ json }) => ({
            data: json.data,
            total: json.total,
        }));
    },
    getOne: (resource, params) => {
        return customDataProvider.getOne(`${resource}`, params);
    },
    getMany: (resource, params) => {
        return customDataProvider.getMany(`${resource}`, params);
    },
    getManyReference: (resource, params) => {
        return customDataProvider.getManyReference(`${resource}`, params);
    },
    update: (resource, params) => {
        return customDataProvider.update(`${resource}`, params);
    },
    updateMany: (resource, params) => {
        return customDataProvider.updateMany(`${resource}/`, params);
    },
    create: (resource, params) => {
        return customDataProvider.create(`${resource}/`, params);
    },
    delete: (resource, params) => {
        return customDataProvider.delete(`${resource}`, params);
    },
    deleteMany: (resource, params) => {
        return customDataProvider.deleteMany(`${resource}/`, params);
    },
};

export default fixedDataProvider;
