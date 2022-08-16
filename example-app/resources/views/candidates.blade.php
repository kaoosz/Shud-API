@extends('layout')
@section('content')
<div class="container">
    <div class="row">
        <div class="col-md-10">
            <div class="card">
                <div class="card-header">
                    <h2>Candidatos Pesquisa</h2>
                </div>
                <form>
                    <label for="search">Search</label>
                    <div>
                      <div>
                      </div>
                      <input id="search" name="search" value="{{ request('search') }}" class="form-input block w-full pl-10 sm:text-sm sm:leading-5" placeholder="Search..." autofocus />
                    </div>
                </form>
                <div class="card-body">
                    <br/>
                    <br/>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Nome Candidato</th>
                                    <th>Nome Urna Candidato</th>
                                    <th>CPF</th>
                                    <th>Ano</th>
                                    <th>Data Nascimento</th>
                                    <th>UE</th>
                                    <th>Estado</th>
                                </tr>
                            </thead>
                            <tbody>
                            @foreach( $can as $c)
                            <tr>
                                <td>{{ $loop->iteration }}</td>
                                <td>{{ $c->NM_CANDIDATO }}</td>
                                <td>{{ $c->NM_URNA_CANDIDATO }}</td>
                                <td>{{ $c->NR_CPF_CANDIDATO }}</td>
                                <td>{{ $c->ANO_ELEICAO }}</td>
                                <td>{{ $c->DT_NASCIMENTO }}</td>
                                <td>{{ $c->NM_UE }}</td>
                                <td>{{ $c->SG_UF }}</td>
                            </tr>
                            @endforeach
                            </tbody>
                        </table>
                        {{$can->links()}}
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
