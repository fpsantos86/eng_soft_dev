import { Admin, Resource, List, Datagrid, TextField, EditButton, DeleteButton, Create, Edit, SimpleForm, TextInput, NumberInput } from 'react-admin';
import fixedDataProvider from './fixedDataProvider';
import React from 'react';

export default function App() {
  return (

    <Admin dataProvider={fixedDataProvider}>
      <Resource
        name='produtos'
        list={ListaDeProdutos}
        create={CadastrarProduto}
        edit={EdicaoDoProduto}
      />
    </Admin>
  );
}

const ListaDeProdutos = (props) => {
  return (
    <List {...props}>
      <Datagrid>
        <TextField source='id' />
        <TextField source='nome' />
        <TextField source='descricao' />
        <TextField source='preco' />
        <TextField source='quantidade_estoque' />
        <EditButton basePath='/produtos' />
        <DeleteButton basePath='/produtos' />
      </Datagrid>
    </List>
  )
}

const CadastrarProduto = (props) => {
  return (
    <Create title='Cadastrar um produto' {...props}>
      <SimpleForm>
        <TextInput source='nome' />
        <TextInput source='descricao' />
        <NumberInput source='preco' />
        <NumberInput source='quantidade_estoque' />
      </SimpleForm>
    </Create>
  )
}

const EdicaoDoProduto = (props) => {
  return (
    <Edit title='Editar produto' {...props}>
      <SimpleForm>
        <TextInput disabled source='id' />
        <TextInput source='nome' />
        <TextInput source='descricao' />
        <NumberInput source='preco' />
        <NumberInput source='quantidade_estoque' />
      </SimpleForm>
    </Edit>
  )
}

