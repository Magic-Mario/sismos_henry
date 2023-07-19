
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    chile = ['Chile']
    japon = ['Japan']
    us_estados = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
             'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
             'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
             'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
             'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
             'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
             'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
             'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
             'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

    # Reemplazar valores NaN con cadena vacía
    data['Lugar'] = data['Lugar'].fillna('')

    # Filtrar por países y estados
    data = data[data['Lugar'].str.contains('|'.join(chile + japon + us_estados))]

    return data

