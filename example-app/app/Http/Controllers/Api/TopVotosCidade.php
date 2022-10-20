<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\VotesCitiesResource2020;
use App\Models\VotesCities_2020;
use App\Models\VotesCities_2018;
use App\Models\VotesCities_2016;
use App\Models\VotesCities_2014;
use App\Models\VotesCities_2012;
use Illuminate\Http\Request;

class TopVotosCidade extends Controller
{

    // fazer um cache aqui pra testar em todos
    public function CidadeMaisVotada()
    {
        if(request()->get('top_cidade')){
            if(request()->get('top_cidade') == 'cidade2020'){
                $option = VotesCities_2020::class;
            }else if(request()->get('top_cidade') == 'cidade2018'){
                $option = VotesCities_2018::class;
            }else if(request()->get('top_cidade') == 'cidade2016'){
                $option = VotesCities_2016::class;
            }else if(request()->get('top_cidade') == 'cidade2014'){
                $option = VotesCities_2014::class;
            }else if(request()->get('top_cidade') == 'cidade2012'){
                $option = VotesCities_2012::class;
            }else
                {
                    return 'Informe bairro.. ex: cidade2018';
                }

            if(request()->has('top_cidade','amount')){

                $var = $option::orderBy('QT_VOTOS','desc')
                ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
                ->when(request()->get('municipio'),function($query){
                    $query->where('NM_MUNICIPIO',request()->get('municipio'));
                })
                ->when(request()->get('cargo'),function($query){
                    $query->where('DS_CARGO_PERGUNTA',request()->get('cargo'));
                })
                ->when(request()->only('top_cidade'),function($query){
                    return $query->take(1000);
                })
                ->get();

                return VotesCitiesResource2020::collection($var->unique('NM_VOTAVEL')->take(request()->get('amount')));

            }

        }

    }
}
