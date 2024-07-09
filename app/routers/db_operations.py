from fastapi import status, Depends, Body, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. csv_handler import CSVHandler
from .. database import get_sql_db
import app.schemas as schemas
import app.models as models

router = APIRouter(tags=["db_operations"], prefix="/transactions")

#TODO: check ruff
"""Revised Plan
Load and Clean CSV: Load the CSV file and process it.
Rename Columns: Rename the DataFrame columns to match the SQLAlchemy model attributes.
Convert DataFrame to Dictionary: Convert the DataFrame to a list of dictionaries.
Create and Add Transactions: Iterate over the dictionaries, create Transaction model instances, and add them to the database."""

@router.post("/add_csv",response_model=schemas.ReturnedTransaction, status_code=status.HTTP_201_CREATED)
def add_csv( db: Session = Depends(get_sql_db)):
        
        path_to_csv = '/Users/sylwestersojka/Documents/HomeBudget/Transactions.csv'
        csv_instance = CSVHandler(path_to_csv)
        df = csv_instance.load_csv()
        new_df = csv_instance.create_df_for_db(df)

        df_to_dict = new_df.to_dict(orient='index')

        print(df_to_dict[0])
    
        new_transaction = models.Transaction(
                **df_to_dict[0]
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return new_transaction



@router.get("/get_transactions", response_model=List[schemas.TransactionSchema], status_code=status.HTTP_200_OK)
def get_transactions(db: Session = Depends(get_sql_db)):
    transactions = db.query(models.Transaction).all()
    return transactions


@router.get("/get_transaction_by_id/{id}", response_model=schemas.ReturnedTransaction, status_code=status.HTTP_200_OK)
def get_transaction_by_id(id: int, db: Session = Depends(get_sql_db)):
        transaction = db.query(models.Transaction).filter(models.Transaction.id == id).first()
        if not transaction:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Transaction with id: {id} not found!')
        
        return transaction


@router.post("/add_transaction", response_model=schemas.TransactionSchema, status_code=status.HTTP_201_CREATED)
def add_transaction(transaction: schemas.TransactionSchema, db: Session = Depends(get_sql_db)):
                    new_transaction = models.Transaction(
                            **transaction.model_dump()
                    )
                    db.add(new_transaction)
                    db.commit()
                    db.refresh(new_transaction)

                    
                    return new_transaction


@router.put("/update_transaction/{id}", response_model=schemas.ReturnedTransaction, status_code=status.HTTP_200_OK)
def update_transaction(id: int, transaction_data: schemas.TransactionSchema = Body(...), db: Session = Depends(get_sql_db)):
        transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
        transaction = transaction_query.first()


        if not transaction:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Transaction with id: {id} not found!')
        
        print(f'Transaction_data: {transaction_data.model_dump()}')
        try:
            transaction_query.update(transaction_data.model_dump(), synchronize_session=False)
            db.commit()
        except Exception as e:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Following error occured {str(e)}')
        
        return transaction


@router.patch("/partialupdate_transaction/{id}", response_model=schemas.ReturnedTransaction, status_code=status.HTTP_200_OK)
def partial_update(id: int, transaction_data: schemas.UpdateTransactionSchema = Body(...), db: Session = Depends(get_sql_db)):
        
        transaction_query = db.query(models.Transaction).filter(models.Transaction.id == id)
        transaction = transaction_query.first()

        if not transaction:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Looked transaction not found id: {id}')
        
        transaction_body = transaction_data.model_dump(exclude_unset=True)
        print(f'Printing content for PATCH request: {transaction_body}')

        for k,v in transaction_body.items():
                setattr(transaction,k,v)
        
        db.commit()
        db.refresh(transaction)

        return transaction
        