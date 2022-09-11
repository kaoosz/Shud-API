<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\VotesSchoolsResource;
use App\Models\VotesSchools_2012;
use App\Models\VotesSchools_2014;
use App\Models\VotesSchools_2016;
use App\Models\VotesSchools_2018;
use App\Models\VotesSchools_2020;
use Illuminate\Http\Request;

class TopVotosEscola extends Controller
{
    public function EscolaMaisVotada()
    {

        if(request()->get('top_escola')){
            if(request()->get('top_escola') == 'escola2020'){
                $option = VotesSchools_2020::class;
            }else if(request()->get('top_escola') == 'escola2018'){
                $option = VotesSchools_2018::class;
            }else if(request()->get('top_escola') == 'escola2016'){
                $option = VotesSchools_2016::class;
            }else if(request()->get('top_escola') == 'escola2014'){
                $option = VotesSchools_2014::class;
            }else if(request()->get('top_escola') == 'escola2012'){
                $option = VotesSchools_2012::class;
            }else
                {
                    return 'Informe bairro.. ex: escola2020 ou escola2018';
                }

                if(request()->has('top_escola','amount')){

                    $var = $option::orderBy('QT_VOTOS','desc')
                    ->whereNotIn('NM_VOTAVEL',['NULO','BRANCO'])
                    ->when(request()->get('municipio'),function($query){
                        $query->where('NM_MUNICIPIO',request()->get('municipio'));
                    })
                    ->when(request()->get('cargo'),function($query){
                        $query->where('DS_CARGO_PERGUNTA',request()->get('cargo'));
                    })
                    ->when(request()->only('top_escola'),function($query){
                        return $query->take(1000);
                    })
                    ->get();

                    return VotesSchoolsResource::collection($var->unique('NM_VOTAVEL')->take(request()->get('amount')));
                }

            }else{
                return 'NO DATA';
            }



    }
}
